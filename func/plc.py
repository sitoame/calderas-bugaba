import json
import time

from utilities import json_formatter


def _is_binary_sequence(values):
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int) and value in (0, 1):
            continue
        return False
    return True


def _normalize_field_value(value):
    if isinstance(value, (bytes, bytearray, memoryview)):
        return int.from_bytes(bytes(value), byteorder="little", signed=False)

    if isinstance(value, (list, tuple)):
        if _is_binary_sequence(value):
            bitmask = 0
            for idx, bit in enumerate(value):
                if bool(bit):
                    bitmask |= 1 << idx
            return bitmask
        return str(value)

    return value


def _resolve_write_tag(tag, tag_aliases):
    if tag in tag_aliases:
        return tag
    for raw_tag, alias in tag_aliases.items():
        if tag == alias:
            return raw_tag
    return None


def _coerce_write_value(value, tag):
    if isinstance(tag, str):
        if tag.startswith("AWB["):
            return _coerce_write_boolean(value)
        if tag.startswith("AWR["):
            return _coerce_write_analog(value)

    if isinstance(value, (bool, int, float)):
        return value

    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "false"):
            return normalized == "true"
        try:
            return int(normalized)
        except ValueError:
            pass
        try:
            return float(normalized)
        except ValueError:
            return value

    return value


def _coerce_write_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "false"):
            return normalized == "true"
        if normalized in ("1", "0"):
            return normalized == "1"
    return None


def _coerce_write_analog(value):
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        try:
            return int(normalized)
        except ValueError:
            pass
        try:
            return float(normalized)
        except ValueError:
            return None
    return None


def _parse_write_payload(raw, tag_aliases):
    if raw is None:
        return None

    if isinstance(raw, (bytes, bytearray, memoryview)):
        raw = bytes(raw).decode("utf-8", errors="ignore")

    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return None
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return None

    if not isinstance(raw, dict):
        return None

    tag = raw.get("tag") or raw.get("field")
    if not tag:
        return None

    resolved_tag = _resolve_write_tag(tag, tag_aliases)
    if resolved_tag is None:
        return None

    value = _coerce_write_value(raw.get("value"), resolved_tag)
    if value is None:
        return None

    return resolved_tag, value


def _build_payload(results, tags_map):
    payload = {}
    for result in results:
        if result is None:
            continue
        if getattr(result, "error", None):
            continue
        tag = getattr(result, "tag", None)
        if tag is None:
            continue
        field_name = tags_map.get(tag, tag)
        payload[field_name] = _normalize_field_value(result.value)
    return payload


def plc_reading(plc_ip, tags_map, cola, name, loop_interval=10):
    """
    Lee en bucle los tags configurados del PLC Allen-Bradley usando LogixDriver.
    Publica en la cola un JSON {field: value} y espera loop_interval segundos.
    """
    from pycomm3 import LogixDriver

    if not tags_map:
        print(f"[{name}] No hay tags configurados para lectura.")
        time.sleep(loop_interval)
        return

    tags = list(tags_map.keys())
    backoffs = [1, 2, 5, 10, 20]
    next_backoff_idx = 0

    while True:
        try:
            with LogixDriver(plc_ip) as plc:
                next_backoff_idx = 0
                while True:
                    results = plc.read(*tags)
                    payload = _build_payload(results, tags_map)

                    if payload:
                        cola.put(json_formatter.formatJson(payload, name))

                    time.sleep(loop_interval)
        except Exception as exc:
            wait_s = backoffs[min(next_backoff_idx, len(backoffs) - 1)]
            print(f"[{name}] PLC error: {exc} — reintentando en {wait_s}s")
            time.sleep(wait_s)
            next_backoff_idx = min(next_backoff_idx + 1, len(backoffs) - 1)


def plc_write_listener(plc_ip, tag_aliases, mqtt_config, name):
    from pycomm3 import LogixDriver
    import paho.mqtt.client as mqtt

    broker = mqtt_config.get("broker")
    port = int(mqtt_config.get("port", 1883))
    topic = mqtt_config.get("topic")
    username = mqtt_config.get("username")
    password = mqtt_config.get("password")

    if not broker or not topic:
        print(f"[{name}] MQTT sin configuración válida para escritura.")
        return

    client = mqtt.Client(client_id=f"plc-writer-{name}")
    if username:
        client.username_pw_set(username, password)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(topic)
            print(f"[{name}] MQTT conectado y suscrito a {topic}")
        else:
            print(f"[{name}] MQTT conexión fallida (rc={rc})")

    def on_message(client, userdata, msg):
        record = _parse_write_payload(msg.payload, tag_aliases)
        if record is None:
            print(f"[{name}] MQTT payload inválido: {msg.payload!r}")
            return
        tag, value = record
        try:
            with LogixDriver(plc_ip) as plc:
                plc.write((tag, value))
            print(f"[{name}] Escrito {tag}={value}")
        except Exception as exc:
            print(f"[{name}] Error escribiendo {tag}: {exc}")

    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            client.connect(broker, port, keepalive=30)
            client.loop_forever()
        except Exception as exc:
            print(f"[{name}] MQTT error: {exc} — reintentando en 5s")
            time.sleep(5)
