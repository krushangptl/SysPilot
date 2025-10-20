#!/usr/bin/env python3

import os
import subprocess
import psutil
from datetime import datetime

HOME = os.path.expanduser("~")
LOG_DIR = os.path.join(HOME, ".Monitor")
LOG_FILE = os.path.join(LOG_DIR, "temperatures.log")
os.makedirs(LOG_DIR, exist_ok=True)

ALERT_TEMP_THRESHOLD = 85


# helper function
def send_notification(title, message):
    subprocess.run(["zenity", "--warning", "--title", title, "--text", message])
    subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"])


def main():
    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    temps = psutil.sensors_temperatures(fahrenheit=False)

    if not temps:
        with open(LOG_FILE, "a") as file:
            file.write(f"{now} | No sensors detected.\n")
        return

    log_line, high_temp = [], []

    for name, entries in temps.items():
        for entry in entries:
            label = entry.label or name
            current = entry.current
            high = entry.high if entry.high else "?"
            crit = entry.critical if entry.critical else "?"

            line = f"{now} | {label}: {current:.1f}°C (High: {high}, Crit: {crit})"
            log_line.append(line)

            if current > ALERT_TEMP_THRESHOLD:
                high_temp.append((label, current))

    with open(LOG_FILE, "a") as file:
        file.write("\n".join(log_line) + "\n")

    if high_temp:
        alert_text = "\n".join([f"{label}: {temps:.1f}°C" for label, temp in high_temp])
        send_notification(
            "High Temperature Alert",
            f"The following component are overheating:\n\n{alert_text}\n\n"
            f"Threshold: {ALERT_TEMP_THRESHOLD}°C",
        )


if __name__ == "__main__":
    main()
