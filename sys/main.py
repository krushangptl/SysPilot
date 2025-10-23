#!/usr/bin/env python3
import time
from . import battery, cpu, ram, disk, temperatures

CHECK_INTERVAL = 5 * 60

MODULES = [battery, cpu, ram, disk, temperatures]


def run_Monitors():
    for module in MODULES:
        try:
            module.main()
        except Exception as err:
            print(f"[ERROR] {module.__name__}: {err}")


def main():
    while True:
        run_Monitors()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
