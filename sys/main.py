#!/usr/bin/env python3
import time
import os
import battery, cpu, ram, disk, temperatures
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

MODULES = [battery, cpu, ram, disk, temperatures]

HOME = os.path.expanduser("~")
LOG_DIR = os.path.join(HOME, ".Monitor")
LOG_FILE = os.path.join(LOG_DIR, "Monitor.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)


def run_Modules(module):
    try:
        module.main()
    except Exception as err:
        print(f"[ERROR] {module.__name__}: {err}")


def run_Monitors():
    with ThreadPoolExecutor(max_workers=len(MODULES)) as executer:
        futures = [executer.submit(run_Modules, m) for m in MODULES]
        for _ in as_completed(futures):
            pass


def main():
    run_Monitors()


if __name__ == "__main__":
    main()
