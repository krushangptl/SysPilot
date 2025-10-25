# Syspilot Setup and Configuration Guide

## 1. Prerequisites

```bash
# Ubuntu / Debian
sudo apt install python3 python3-pip libnotify-bin zenity upower

# Fedora / RHEL
sudo dnf install python3 python3-pip libnotify zenity upower

# Arch Linux
sudo pacman -S python python-pip libnotify zenity upower
```

---

## 2. Clone & Installation

```bash
git clone https://github.com/krushangptl/syspilot.git
cd syspilot
pip install -r requirments.txt
```

---

## 3. Module Testing

```bash
cd sys
python3 cpu.py
python3 ram.py
python3 disk.py
python3 temperatures.py
python3 battery.py  # skip if no battery hardware/desktop
```

## 4. Main Orchestrator

```bash
python3 main.py
ls -lh ~/.Monitor/
tail -f ~/.Monitor/*.log
```

---

## 5. Systemd User Service

1. Update `config/syspilot.service` to point to absolute path of `main.py`.
2. Create user service directory:

```bash
mkdir -p ~/.config/systemd/user/
cp config/syspilot.service ~/.config/systemd/user/
cp config/syspilot.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now syspilot.timer
```

3. Verify:

```bash
systemctl --user status syspilot.service
systemctl --user list-timers --all | grep syspilot
```

---

## 6. Configuration

- Edit thresholds in `sys/*.py` (CPU, RAM, Disk, Battery, Temperature)
- Adjust monitoring interval in `config/syspilot.timer`
- Customize notification (`notify-send`/`zenity`) or disable audio

---

## 7. Logs

Default Location: ~/.Monitor/

```bash
~/.Monitor/
├── cpu_usage.log
├── ram_usage.log
├── disk_usage.log
├── temperatures.log
├── battery_health.log
└── Monitor.log
```

---

## 8. Troubleshooting

| Issue                     | Fix                                             |
| ------------------------- | ----------------------------------------------- |
| No notifications          | Ensure `dunst` / notification-daemon is running |
| Missing logs              | Check `~/.Monitor` write permissions            |
| Battery errors on desktop | Expected behavior (no battery)                  |
| High CPU usage            | Increase timer interval (`OnUnitActiveSec`)     |

---
