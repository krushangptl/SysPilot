#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

# dir and log file setup
HOME = os.path.expanduser("~")
LOG_DIR = os.path.join(HOME, ".Monitor")
os.makedirs(LOG_DIR, exist_ok=True)


def get_log_path(filename: str) -> str:
    return os.path.join(LOG_DIR, filename)


# timing
def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d | %H:%M:%S")


# run command from script
def run_cmds(cmd) -> str:
    try:
        return subprocess.check_output(cmd.split(), text=True).strip()
    except subprocess.CalledProcessError:
        return ""


# notification with zenity
def zenity_notification(title, message, kind, sound=True):
    cmd = ["zenity", f"--{kind}", "--title", title, "--text", message]
    if kind == "info":
        subprocess.Popen(cmd)
        if sound:
            subprocess.Popen(
                ["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"]
            )
    elif kind == "warning":
        subprocess.Popen(cmd)
        if sound:
            subprocess.Popen(
                ["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"]
            )
    # bell sound for notification


# notification with notify
def notify_send_notification(title, message, sound=True):
    cmd = ["notify-send", title, message]
    subprocess.Popen(cmd)
    if sound:
        subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"])
