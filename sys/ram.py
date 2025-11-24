#!/usr/bin/env python3

import psutil
from utils import get_log_path, notify_send_notification, timestamp

LOG_FILE = get_log_path("ram_usage.log")

ALERT_RAM_THRESHOLD = 85  # % usage
ALERT_SWAP_THRESHOLD = 70  # % usage


def main():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    ram_used_gb = ram.used / (1024**3)
    ram_total_gb = ram.total / (1024**3)
    swap_used_gb = swap.used / (1024**3)
    swap_total_gb = swap.total / (1024**3)

    if ram.percent > ALERT_RAM_THRESHOLD:
        notify_send_notification(
            "High RAM Usage",
            f"RAM Usage: {ram.percent:.1f}% ({ram_used_gb:.2f}/{ram_total_gb:.2f} GB)",
            True,
        )

    if swap.percent > ALERT_SWAP_THRESHOLD:
        notify_send_notification(
            "High SWAP Usage",
            f"SWAP Usage: {swap.percent:.1f}% ({swap_used_gb:.2f}/{swap_total_gb:.2f} GB)",
            True,
        )

    now = timestamp()
    log_line = (
        f"{now} | RAM: {ram.percent:.1f}% ({ram_used_gb:.2f}/{ram_total_gb:.2f} GB) "
        f"| SWAP: {swap.percent:.1f}% ({swap_used_gb:.2f}/{swap_total_gb:.2f} GB)"
    )

    with open(LOG_FILE, "a") as file:
        file.write(log_line + "\n")


if __name__ == "__main__":
    main()
