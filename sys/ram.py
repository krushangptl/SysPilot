#!/usr/bin/env python3

import os
import subprocess
import psutil
from datetime import datetime

# settings
HOME = os.path.expanduser("~")
LOG_DIR = os.path.join(HOME, ".Monitor")
LOG_FILE = os.path.join(LOG_DIR, "ram_usage.log")
os.makedirs(LOG_DIR, exist_ok=True)

ALERT_RAM_THRESHOLD = 85  # % usage
ALERT_SWAP_THRESHOL = 70  # % usage


# helper function
def send_notification(title, message):
    subprocess.run(["notify-send", title, message])


def main():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    ram_used_gb = ram.used / (1024**3)
    ram_total_gb = ram.total / (1024**3)
    swap_used_gb = swap.used / (1024**3)
    swap_total_gb = swap.total / (1024**3)

    if ram.percent > ALERT_RAM_THRESHOLD:
        send_notification(
            "High RAM Usage",
            f"RAM Usage: {ram.percent:.1f}% ({ram_used_gb:.2f}/{ram_total_gb:.2f} GB)",
        )

    if swap.percent > ALERT_SWAP_THRESHOL:
        send_notification(
            "High SWAP Usage",
            f"SWAP Usage: {swap.percent:.1f}% ({swap_used_gb:.2f}/{swap_total_gb:.2f} GB)",
        )

    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    log_line = (
        f"{now} | RAM: {ram.percent:.1f}% ({ram_used_gb:.2f}/{ram_total_gb:.2f}) GB) "
        f"| SWAP: {swap.percent:.1f}% ({swap_used_gb:.2f}/{swap_total_gb:.2f}) GB)"
    )

    with open(LOG_FILE, "a") as file:
        file.write(log_line + "\n")


if __name__ == "__main__":
    main()
