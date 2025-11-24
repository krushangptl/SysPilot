#!/usr/bin/env python3

import psutil
from utils import get_log_path, notify_send_notification, timestamp

LOG_FILE = get_log_path("disk_usage.log")

ALERT_DISK_THRESHOLD = 85  # % usage


def main():
    partitions = psutil.disk_partitions(all=False)

    log_line = []
    now = timestamp()
    for part in partitions:
        if "snap" in part.mountpoint or part.fstype == "":
            continue

        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue

        used_gb = usage.used / (1024**3)
        total_gb = usage.total / (1024**3)
        percent = usage.percent

        if percent > ALERT_DISK_THRESHOLD:
            notify_send_notification(
                "Disk Space Alert",
                f"Mount {part.mountpoint} is {percent:.1f}% full "
                f"({used_gb:.2f}/{total_gb:.2f} GB)",
                True,
            )

        log_line.append(
            f"{now} | {part.device} {part.mountpoint} | {percent:.1f}% used "
            f"({used_gb:.2f}/{total_gb:.2f} GB)"
        )

    with open(LOG_FILE, "a") as file:
        for line in log_line:
            file.write(line + "\n")


if __name__ == "__main__":
    main()
