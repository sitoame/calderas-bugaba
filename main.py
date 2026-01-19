#!/usr/bin/env python3
import os
import signal
import time
import multiprocessing as mp
from datetime import datetime
from multiprocessing import shared_memory

from func import modbus
from var import const, regist
from utilities import write_data


def start():
    print(f"[BOOT] {const.NOMBRE} v{const.VERSION} — {datetime.now()}", flush=True)
    target_map = getattr(const, 'mbus_targets', None) or {
        name: {'ip': addr, 'port': const.mbus_gwy_port, 'slave_id': const.mbus_gwy_slv_id}
        for name, addr in const.mbus_gwy_ip.items()
    }
    printable_targets = {
        name: {k: v for k, v in cfg.items() if k in ('ip', 'port', 'slave_id')}
        for name, cfg in target_map.items()
    }
    print(f"[BOOT] Destinos Modbus: {printable_targets}", flush=True)

    processes = []
    shared_segments = []

    for name, cfg in target_map.items():
        address = cfg.get('ip')
        port = cfg.get('port', const.mbus_gwy_port)
        slave_id = cfg.get('slave_id', const.mbus_gwy_slv_id)
        q = mp.Queue()
        shm = shared_memory.SharedMemory(create=True, size=regist._DSE.nbytes)
        shared_segments.append(shm)

        reader = mp.Process(
            target=modbus.DSE_modbus_reading,
            args=(shm, regist._DSE, address, port, slave_id, q, name),
            daemon=True,
            name=f"reader:{name}",
        )

        writer = mp.Process(
            target=write_data.writeData,
            args=(q, name),
            daemon=True,
            name=f"writer:{name}",
        )

        reader.start()
        writer.start()
        processes.extend([reader, writer])

    def _graceful_exit(signum=None, frame=None):
        print("[SHUTDOWN] Señal recibida, cerrando procesos…", flush=True)
        for proc in processes:
            if proc.is_alive():
                proc.terminate()
        for proc in processes:
            try:
                proc.join(timeout=5)
            except Exception:
                pass
            if proc.is_alive():
                try:
                    proc.kill()
                except Exception:
                    pass
        for shm in shared_segments:
            try:
                shm.close()
                shm.unlink()
            except FileNotFoundError:
                pass
        os._exit(0)

    signal.signal(signal.SIGINT, _graceful_exit)
    signal.signal(signal.SIGTERM, _graceful_exit)

    while True:
        for proc in processes:
            if not proc.is_alive():
                print(f"[WARN] Proceso caído: {proc.name} (exitcode={proc.exitcode})", flush=True)
        time.sleep(2)


if __name__ == "__main__":
    try:
        mp.set_start_method("fork")
    except RuntimeError:
        pass

    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    print(f"Task started at {datetime.now()}", flush=True)
    start()
