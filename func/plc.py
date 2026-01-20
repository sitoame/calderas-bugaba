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
