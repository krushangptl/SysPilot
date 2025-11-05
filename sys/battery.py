#!/usr/bin/env python3

from datetime import datetime, timedelta
from utils import get_log_path, run_cmds, zenity_notification, timestamp

LOG_FILE = get_log_path("battery_health.log")

# timing
TODAY = timestamp()
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


# get battery info
def battery_hardware_info():
    try:
        BAT_PATH = run_cmds("upower -e | grep 'BAT'")
        BAT_INFO = run_cmds(f"upower -i {BAT_PATH}")
        return BAT_INFO
    except Exception as err:
        print(f"Error getting battery info: {err}")
        return None


# extracting info from battery info
def battery_info(info):
    data = dict()
    for line in info.splitlines():
        line = line.strip()
        if line.startswith("state:"):
            data["state"] = line.split(":")[1].strip()
        elif line.startswith("energy-full:"):
            data["energy_full"] = float(line.split(":")[1].strip().split(" ")[0])
        elif line.startswith("energy-full-design:"):
            data["energy_design"] = float(line.split(":")[1].strip().split(" ")[0])
        elif line.startswith("percentage:"):
            data["percentage"] = float(line.split(":")[1].strip().strip("%"))
        elif line.startswith("capacity:"):
            data["health"] = float(line.split(":")[1].strip().strip("%"))
    return data


# alert logic
def battery_alerts(battery):
    if not battery:
        return

    if battery["percentage"] <= 20 and battery["state"] == "discharging":
        zenity_notification(
            "Battery Low",
            f"Charge is at {battery['percentage']}% - please Plug in!",
            "warning",
        )
    elif battery["percentage"] >= 80 and battery["state"] == "charging":
        zenity_notification(
            "Battery High",
            f"Charge is at {battery['percentage']}% - consider unplug to preserve health!",
            "info",
        )


# compare with yesterday condition
def compare_yesterday(battery):
    try:
        with open(LOG_FILE) as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    yesterday_lines = [line for line in lines if line.startswith(YESTERDAY)]
    if yesterday_lines:
        yesterday_health = float(
            yesterday_lines[-1].split("|")[-1].split(":")[1].strip().strip("%")
        )
        if battery["health"] < yesterday_health:
            LOSS = round(yesterday_health - battery["health"], 2)
            zenity_notification(
                "Battery Health Drop",
                f"Health decreased by {LOSS}% since yesterday ?! (Now: {battery['health']}%)",
                "warning",
            )


# log battery data
def log_battery(battery):
    if not battery:
        return

    # today's log data
    log_line = f"{TODAY} | Charge: {battery['percentage']}% | Full: {battery['energy_full']} Wh | Design: {battery['energy_design']} Wh | Health: {battery['health']}%\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_line)


def main():
    info = battery_hardware_info()
    battery = battery_info(info)

    if not battery:
        print("Unable to read battery info")
        return 1

    # alerts
    battery_alerts(battery)

    # change or no change
    compare_yesterday(battery)

    # writting logs
    log_battery(battery)


if __name__ == "__main__":
    exit(main())
