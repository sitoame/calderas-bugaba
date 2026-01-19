import time
from datetime import datetime
from socket import create_connection
from collections import defaultdict
from numpy import ndarray
from umodbus.client import tcp  # pip install umodbus
from func import math as dse_math  # utilidades de decodificación locales
from utilities import json_formatter

# ----------------------------
# Construcción de bloques de lectura
# ----------------------------
def group_by_page(addresses0):
    """
    Agrupa direcciones (0-based) por página GenComm (256 regs/página)
    y construye rangos contiguos con qty <= 125 (límite Modbus).
    Devuelve lista de chunks: [{'start': int, 'qty': int, 'addrs': set(...)}]
    """
    pages = defaultdict(list)
    for a in sorted(set(addresses0)):
        pages[a // 256].append(a)

    chunks = []
    for _, addrs in pages.items():
        i = 0
        n = len(addrs)
        while i < n:
            start = addrs[i]
            end = start
            # Extiende mientras sean contiguos y qty <= 125
            while (i + 1 < n) and (addrs[i + 1] == end + 1) and ((addrs[i + 1] - start + 1) <= 125):
                i += 1
                end = addrs[i]
            qty = end - start + 1
            chunks.append({'start': start, 'qty': qty, 'addrs': set(range(start, end + 1))})
            i += 1
    return chunks

def build_read_plan(array_):
    """
    A partir del array de registros, devuelve:
      - chunks de lectura (por página)
      - conjunto all_addr0 (todas las direcciones a leer, 0-based)
    Incluye las direcciones +1 para 32-bit.
    """
    addr0_list = []
    need_next = set()
    for row in array_:
        addr_abs = int(row['address'])
        addr0 = dse_math.normalize_addr_0based(addr_abs)
        addr0_list.append(addr0)
        name = row['data']
        if name in dse_math.FIELDS_32:
            need_next.add(addr0 + 1)

    all_addr0 = sorted(set(addr0_list) | need_next)
    chunks = group_by_page(all_addr0)
    return chunks, set(all_addr0)

# ----------------------------
# Lector principal (loop con reconexión)
# ----------------------------
def DSE_modbus_reading(_shm, array_, mbus_gwy_ip, mbus_gwy_port, mbus_gwy_slv_id, cola, name,
                       loop_interval=10, connect_timeout=2.0):
    """
    Lee en bucle los registros de 'array_' (struct de regist.y),
    decodifica y publica un JSON {field: value} en 'cola'.
    Reintenta conexión con backoff ante fallo.
    """
    # Copia compartida del array en memoria compartida
    array = ndarray(array_.shape, dtype=array_.dtype, buffer=_shm.buf)
    array[:] = array_[:]

    # Plan de lectura (estático salvo que cambie el array)
    chunks, all_addr0 = build_read_plan(array)

    backoffs = [1, 2, 5, 10, 20]  # segundos
    while True:
        try:
            with create_connection((mbus_gwy_ip, mbus_gwy_port), connect_timeout) as sock:
                # Si conecta, resetea el backoff
                next_backoff_idx = 0
                while True:
                    # 1) Leer todos los bloques
                    regs_dict = {}
                    for ch in chunks:
                        msg = tcp.read_holding_registers(
                            slave_id=mbus_gwy_slv_id,
                            starting_address=ch['start'],   # 0-based
                            quantity=ch['qty']
                        )
                        resp = tcp.send_message(msg, sock)  # lista de enteros (regs)
                        # Mapear al dict global
                        for i, val in enumerate(resp):
                            regs_dict[ch['start'] + i] = val

                    # 2) Decodificar y actualizar array campo por campo
                    payload_fields = {}
                    for row in array:
                        addr_abs = int(row['address'])
                        dtype    = str(row['type'])
                        field    = str(row['data'])
                        decimal  = float(row['decimal'])
                        addr0    = dse_math.normalize_addr_0based(addr_abs)

                        try:
                            val, is_default = dse_math.extract_value(field, dtype, decimal, regs_dict, addr0)
                            if val is None or is_default:
                                continue
                            row['value'] = float(val)
                            payload_fields[field] = row['value']
                        except Exception:
                            # No interrumpir por un valor individual
                            pass

                    if not payload_fields:
                        # Evita ingestar lecturas vacías o con solo valores por defecto
                        time.sleep(loop_interval)
                        continue

                    # 3) Publicar a la cola (JSON simple)
                    #print(f"[{datetime.now()}] {name} payload → {payload_fields}", flush=True)
                    cola.put(json_formatter.formatJson(payload_fields, name))

                    time.sleep(loop_interval)
        except Exception as e:
            # Error de conexión/lectura: backoff y reintento
            wait_s = backoffs[min(next_backoff_idx if 'next_backoff_idx' in locals() else 0, len(backoffs) - 1)]
            print(f"[{name}] Modbus error: {e} — reintentando en {wait_s}s")
            time.sleep(wait_s)
            if 'next_backoff_idx' in locals():
                next_backoff_idx = min(next_backoff_idx + 1, len(backoffs) - 1)
            else:
                next_backoff_idx = 1
