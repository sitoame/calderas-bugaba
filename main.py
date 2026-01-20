#!/usr/bin/env python3
import os
import signal
import time
import multiprocessing as mp
from datetime import datetime

from func import plc
from var import const
from utilities import write_data


def start():
    print(f"[BOOT] {const.NOMBRE} v{const.VERSION} — {datetime.now()}", flush=True)
    target_map = getattr(const, 'plc_targets', None) or {
        name: {'ip': addr}
        for name, addr in const.plc_ip.items()
    }
    printable_targets = {
        name: {k: v for k, v in cfg.items() if k in ('ip',)}
        for name, cfg in target_map.items()
    }
    print(f"[BOOT] Destinos PLC: {printable_targets}", flush=True)

    processes = []

    for name, cfg in target_map.items():
        address = cfg.get('ip')
        q = mp.Queue()

        reader = mp.Process(
            target=plc.plc_reading,
            args=(address, const.plc_tags, q, name),
            daemon=True,
            name=f"reader:{name}",
        )

        writer = mp.Process(
            target=write_data.writeData,
            args=(q, name),
            daemon=True,
            name=f"writer:{name}",
        )

        mqtt_cfg = dict(const.mqtt_config)
        mqtt_cfg["topic"] = const.mqtt_write_topics.get(name)
        plc_writer = mp.Process(
            target=plc.plc_write_listener,
            args=(address, const.plc_write_tags, mqtt_cfg, name),
            daemon=True,
            name=f"plc-writer:{name}",
        )

        reader.start()
        writer.start()
        plc_writer.start()
        processes.extend([reader, writer, plc_writer])

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
