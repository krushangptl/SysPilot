#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime, timedelta

# dir and log file setup
HOME = os.path.expanduser("~")
LOG_DIR = os.path.join(HOME, ".Monitor")
LOG_FILE = os.path.join(LOG_DIR, "battery_health.log")

os.makedirs(LOG_DIR, exist_ok=True)

# dates and time
TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


# helper functio
def run_cmds(cmd):
    """Run a shell command and return its output"""
    return subprocess.check_output(cmd, shell=True, text=True).strip()


def send_notification(title, message, type_="info"):
    """Send a desktop notification via zenity"""
    if type_ == "info":
        subprocess.run(["zenity", "--info", "--title", title, "--text", message])
    elif type_ == "warning":
        subprocess.run(["zenity", "--warning", "--title", title, "--text", message])
    # Play sound for notification
    subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"])


# battery info

BATTERY_PATH = run_cmds("upower -e | grep BAT")
BAT_INFO = run_cmds(f"upower -i {BATTERY_PATH}")


def parse_upower_output(info):
    """Extract values from upower output"""
    data = dict()
    for line in info.splitlines():
        line = line.strip()
        if line.startswith("state:"):
            data["state"] = line.split(":", 1)[1].strip()
        elif line.startswith("percentage:"):
            data["percentage"] = float(line.split(":", 1)[1].strip().strip("%"))
        elif line.startswith("energy-full:"):
            data["energy_full"] = float(line.split(":", 1)[1].strip().split()[0])
        elif line.startswith("energy-full-design:"):
            data["energy_design"] = float(line.split(":", 1)[1].strip().split()[0])
    return data


battery = parse_upower_output(BAT_INFO)

# validate numeric values
if "energy_full" not in battery or "energy_design" not in battery:
    print("Error: Unable to read energy values from upower output")
    exit(1)

HEALTH = round((battery["energy_full"] / battery["energy_design"]) * 100, 2)

# alerts for charge based on states

if battery["percentage"] < 20 and battery.get("state") == "discharging":
    send_notification(
        "Battery Low",
        f"Charge is at {battery['percentage']}% - please plug in!",
        "warning",
    )

if battery["percentage"] > 80 and battery.get("state") == "charging":
    send_notification(
        "Battery High",
        f"Charge is at {battery['percentage']}% - consider unplugging to preserve health.",
        "info",
    )

# todays log data
log_line = f"{TODAY} | Charge: {battery['percentage']}% | Full: {battery['energy_full']} Wh | Design: {battery['energy_design']} Wh | Health: {HEALTH}%\n"
with open(LOG_FILE, "a") as file:
    file.write(log_line)

# compare with yesterday
try:
    with open(LOG_FILE) as file:
        lines = file.readlines()
except FileNotFoundError:
    lines = []

yesterday_lines = [line for line in lines if line.startswith(YESTERDAY)]
if yesterday_lines:
    yesterday_health = float(yesterday_lines[-1].split("|")[-1].split("%")[0].strip())
    if HEALTH < yesterday_health:
        LOSS = round(yesterday_health - HEALTH, 2)
        send_notification(
            "Battery Health Drop",
            f"Health decreased by {LOSS}% since yesterday (NOW: {HEALTH}%)",
            "warning",
        )
