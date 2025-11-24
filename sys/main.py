#!/usr/bin/env python3
import battery, cpu, ram, disk, temperatures
import logging
from concurrent.futures import ThreadPoolExecutor
from utils import get_log_path

MODULES = [battery, cpu, ram, disk, temperatures]

LOG_FILE = get_log_path("Monitor.log")

logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)


def run_Modules(module):
    try:
        module.main()
    except Exception as err:
        print(f"[ERROR] {module.__name__}: {err}")


def run_Monitors():
    with ThreadPoolExecutor(max_workers=len(MODULES)) as executer:
        futures = [executer.submit(run_Modules, m) for m in MODULES]
        for _ in futures:
            pass


def main():
    run_Monitors()


if __name__ == "__main__":
    main()
