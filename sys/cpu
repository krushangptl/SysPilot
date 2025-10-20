#!/usr/bin/env python3

import psutil
import os
from datetime import datetime
import subprocess
from collections import deque

# settings
HOME = os.path.expanduser("~")
LOG_DIR = os.path.join(HOME, ".Monitor")
LOG_FILE = os.path.join(LOG_DIR, "cpu_usage.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Thresholds
ALERT_CPU_THRESHOLD = 90  # % usage
ALERT_TEMP_THRESHOLD = 85  # celsius
AVG_WINDOW = 5  # number of measurements to avg


# helper function
def send_notification(title, message):
    subprocess.run(["notify-send", title, message])


# store n cpu measurements
cpu_hist = deque(maxlen=AVG_WINDOW)


def main():
    cpu_percent = psutil.cpu_percent(1)
    info_freq = psutil.cpu_freq()
    cpu_freq = info_freq.current if info_freq else 0.0
    cpu_hist.append(cpu_percent)

    avg_cpu = sum(cpu_hist) / len(cpu_hist)

    cpu_temp = None
    try:
        temps = psutil.sensors_temperatures()
        coretemp = temps.get("coretemp", [])
        if coretemp:
            cpu_temp = max([t.current for t in coretemp if t.label.startswith("Core")])
    except Exception:
        cpu_temp = None

    if avg_cpu > ALERT_CPU_THRESHOLD:
        send_notification(
            "High CPU Usage",
            f"Avg CPU Usage over last {AVG_WINDOW} sample: {avg_cpu:.1f}%",
        )

    if cpu_temp > ALERT_TEMP_THRESHOLD:
        send_notification("High CPU Temperature", f"CPU Temperature: {cpu_temp:.1f}°C")

    # log to file
    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    log_line = f"{now} | CPU Usage: {cpu_percent:.1f}% | Avg: {avg_cpu:.1f}% | Freq: {cpu_freq:.1f} MHz"
    if cpu_temp:
        log_line += f" | Temp: {cpu_temp:.1f}°C"
    log_line += "\n"

    with open(LOG_FILE, "a") as file:
        file.write(log_line)


if __name__ == "__main__":
    main()
