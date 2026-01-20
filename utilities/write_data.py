import json
import os
import time
import sqlite3
from datetime import datetime
from queue import Empty

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from utilities import json_formatter
from var import const

loaded_data_per_process = {}
_schema_cache = {}  # cache por tabla: {name: set(columns)}
_client_cache = None
_write_api_cache = None


def _get_write_api():
    """
    Lazily crea un cliente de Influx y devuelve un write_api reutilizable por proceso.
    """
    global _client_cache, _write_api_cache
    if _write_api_cache is None:
        _client_cache = InfluxDBClient(
            url=const.url_influx,
            token=const.api_token_influx,
            org=const.org_influx,
            debug=False,
            timeout=50000,
        )
        _write_api_cache = _client_cache.write_api(write_options=SYNCHRONOUS)
    return _write_api_cache

def _ensure_backup_dir(path):
    base = os.path.dirname(path)
    if base:
        os.makedirs(base, exist_ok=True)


def _normalize_record(raw, default_name):
    """Convierte distintos formatos de mensajes en un dict listo para Influx."""
    if raw is None:
        return None

    if isinstance(raw, bytes):
        raw = raw.decode('utf-8', errors='ignore')

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

    if 'measurement' in raw and 'fields' in raw:
        return _coerce_boolean_fields(raw)

    if 'name' in raw and isinstance(raw.get('data'), dict):
        measurement = raw.get('measurement') or raw['name'] or default_name
        return _coerce_boolean_fields(json_formatter.formatJson(raw['data'], measurement))

    # Si recibimos un simple dict de campos, úsalos como fields
    return _coerce_boolean_fields(json_formatter.formatJson(raw, raw.get('measurement', default_name)))


def _coerce_boolean_fields(record):
    """Convierte fields booleanos a 0/1 para evitar tipos boolean en Influx."""
    fields = record.get('fields')
    if not isinstance(fields, dict):
        return record
    normalized = {}
    for key, value in fields.items():
        normalized[key] = int(value) if isinstance(value, bool) else value
    record['fields'] = normalized
    return record


def _try_get_write_api():
    try:
        return _get_write_api()
    except Exception as exc:
        print(datetime.now(), "No se pudo crear el cliente de Influx:", exc)
        return None


def writeData(cola, name, buffer_size=2, flush_interval=5.0):
    """Lee de la cola, agrupa en lotes y escribe en Influx/SQLite según disponibilidad."""
    pid = os.getpid()
    loaded_data = loaded_data_per_process.setdefault(pid, [])
    db_path = f'/home/maxia/myapp/backup/{name}.db'
    _ensure_backup_dir(db_path)

    write_api = None
    last_flush = time.monotonic()

    while True:
        drained = False
        while True:
            try:
                raw = cola.get_nowait()
            except Empty:
                break

            record = _normalize_record(raw, name)
            if record is not None:
                loaded_data.append(record)
                drained = True

        now = time.monotonic()
        should_flush = loaded_data and (
            len(loaded_data) >= buffer_size or
            (now - last_flush) >= flush_interval
        )

        if should_flush:
            try:
                if write_api is None:
                    write_api = _try_get_write_api()

                if write_api is None:
                    raise RuntimeError("No hay cliente de Influx disponible")

                if os.path.exists(db_path):
                    backlog = get_data_as_json_string_dynamic(name, db_path)
                    if backlog:
                        loaded_data[:0] = backlog

                for i in range(0, len(loaded_data), buffer_size):
                    batch = loaded_data[i:i + buffer_size]
                    write_api.write(bucket=const.bucket_influx, record=batch)

                if os.path.exists(db_path):
                    os.remove(db_path)

                loaded_data.clear()

            except Exception as e:
                print(datetime.now(), f'Fallo en la ingesta a la BD (pid {pid}):', e)
                try:
                    write_in_sqlite_dynamic(name, loaded_data, db_path)
                except Exception as e2:
                    print("Error adicional al escribir en SQLite:", e2)
                loaded_data.clear()
                time.sleep(0.2)

            last_flush = time.monotonic()

        # Evita ocupar CPU cuando no hay datos
        if not drained:
            time.sleep(0.1)


def _ensure_table_and_columns(conn, name, field_keys):
    """
    Crea la tabla si no existe y agrega columnas que falten según field_keys.
    Cachea el esquema en _schema_cache[name].
    """
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (name,))
    exists = cur.fetchone() is not None

    if not exists:
        # Crear tabla con columnas 'time' + campos iniciales
        cols_def = ", ".join([f'"{k}" REAL' for k in field_keys])
        create_sql = f'''
            CREATE TABLE "{name}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time INTEGER,
                {cols_def}
            );
        '''
        cur.execute(create_sql)
        conn.commit()
        _schema_cache[name] = set(field_keys)
        return

    # Si existe, cargar columnas actuales (cache o introspección)
    if name not in _schema_cache:
        cur.execute(f'PRAGMA table_info("{name}");')
        cols = {row[1] for row in cur.fetchall()}  # row[1] = column name
        _schema_cache[name] = cols
    existing = _schema_cache[name]

    # Agregar las que falten
    to_add = [k for k in field_keys if k not in existing]
    for col in to_add:
        cur.execute(f'ALTER TABLE "{name}" ADD COLUMN "{col}" REAL;')
        existing.add(col)
    if to_add:
        conn.commit()


def write_in_sqlite_dynamic(name, data, path):
    """
    Persiste una lista de puntos (measurement, fields, time) en SQLite,
    creando/actualizando columnas dinámicamente.
    """
    if not data:
        return

    # Unión de keys de fields para esta tanda
    all_keys = set()
    for rec in data:
        fields = rec.get('fields', {}) or {}
        all_keys.update(fields.keys())
    # Si no hay fields, nada que hacer
    if not all_keys:
        return

    with sqlite3.connect(path) as conn:
        conn.execute('PRAGMA journal_mode=WAL;')
        _ensure_table_and_columns(conn, name, sorted(all_keys))

        # Preparar insert dinámico (time + todas las cols conocidas)
        cols_sorted = ['time'] + sorted(_schema_cache[name] - {'id', 'time'})
        placeholders = ", ".join(["?"] * len(cols_sorted))
        insert_sql = f'INSERT INTO "{name}" ({", ".join(cols_sorted)}) VALUES ({placeholders});'

        cur = conn.cursor()
        for rec in data:
            fields = rec.get('fields', {}) or {}
            t = rec.get('time')
            row = [t] + [fields.get(col) for col in cols_sorted[1:]]
            cur.execute(insert_sql, row)

        conn.commit()


def get_data_as_json_string_dynamic(name, path):
    """
    Lee TODO lo almacenado en SQLite para 'name' y lo devuelve como lista de
    dicts con la forma esperada por Influx write_api:
      {"measurement": name, "fields": {...}, "time": <time>}
    """
    if not os.path.exists(path):
        return []

    out = []
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        try:
            cur.execute(f'SELECT * FROM "{name}";')
        except sqlite3.Error:
            return []

        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]  # incluye id, time y columnas de fields

        for row in rows:
            record = dict(zip(cols, row))
            t = record.get('time')
            fields = {k: v for k, v in record.items() if k not in ('id', 'time')}
            out.append({
                "measurement": name,
                "fields": fields,
                "time": t
            })
    return out
