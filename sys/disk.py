#!/usr/bin/env python3

import os
import subprocess
import psutil
from datetime import datetime

# settings
HOME = os.path.expanduser("~")
LOG_DIR = os.path.join(HOME, ".Monitor")
LOG_FILE = os.path.join(LOG_DIR, "disk_usage.log")
os.makedirs(LOG_DIR, exist_ok=True)

ALERT_DISK_THRESHOLD = 85  # % usage


# helper function
def send_notification(title, message):
    subprocess.run(["notify-send", title, message])


def main():
    partitions = psutil.disk_partitions(all=False)

    log_line = []
    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")

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
            send_notification(
                "Disk Space Alert",
                f"Mount {part.mountpoint} is {percent:.1f}% full "
                f"({used_gb:.2f}/{total_gb:.2f} GB)",
            )

        log_line.append(
            f"{now} | {part.device} {part.mountpoint} | {percent:.1f}% used "
            f"({used_gb:.2f}/{total_gb:.2f} GB"
        )

    with open(LOG_FILE, "a") as file:
        for line in log_line:
            file.write(line + "\n")


if __name__ == "__main__":
    main()
