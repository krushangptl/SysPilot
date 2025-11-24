#!/usr/bin/env python3

import psutil
from utils import get_log_path, zenity_notification, timestamp

LOG_FILE = get_log_path("temperatures.log")

ALERT_TEMP_THRESHOLD = 85


def main():
    now = timestamp()
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

            if current == 0.0:
                continue

            high = entry.high if entry.high is not None else "?"
            crit = entry.critical if entry.critical is not None else "?"

            line = f"{now} | {label}: {current:.1f}°C (High: {high}, Crit: {crit})"
            log_line.append(line)

            if current > ALERT_TEMP_THRESHOLD:
                high_temp.append((label, current))

    with open(LOG_FILE, "a") as file:
        file.write("\n".join(log_line) + "\n")

    if high_temp:
        alert_text = "\n".join([f"{label}: {temp:.1f}°C" for label, temp in high_temp])
        zenity_notification(
            "High Temperature Alert",
            f"The following component are overheating:\n\n{alert_text}\n\n"
            f"Threshold: {ALERT_TEMP_THRESHOLD}°C",
            "warning",
        )


if __name__ == "__main__":
    main()
