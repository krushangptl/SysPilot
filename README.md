# SysPilot

> **A lightweight, production-ready system monitoring daemon for Linux** - Built for minimalist desktop environments

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)

**SysPilot** is a simple, modular daemon that monitors system resources (CPU, RAM, disk, temperature, battery) and provides desktop notifications for critical thresholds.  
It’s designed for **minimalist Linux environments** like **i3**, **Sway**, or **bspwm**, where traditional GUI monitors are not available.

---

## Project Motivation

Tiling window managers often lack built-in tools to alert users when resources are under stress.  
SysPilot quietly monitors your system and warns you before it overheats, runs out of memory, or drains the battery — **without adding heavy dependencies**.

I built this project to:

- Learn about **systemd user services** and Linux daemon management
- Explore **concurrent programming** and **system resource monitoring**
- Practice **Linux automation** and **fault-tolerant design**

---

## Features

| Feature                   | Description                                         |
| ------------------------- | --------------------------------------------------- |
| **CPU / Temp Monitoring** | Tracks usage and temperature with alerts            |
| **Memory Monitoring**     | RAM and SWAP thresholds with notifications          |
| **Disk Monitoring**       | Multi-partition usage alerts                        |
| **Battery Health**        | Tracks charge % and capacity degradation            |
| **Notifications**         | `notify-send` / `zenity` alerts for critical events |
| **Logging**               | Saves detailed system logs in `~/.Monitor/`         |
| **Systemd Timer**         | Runs automatically in user space (no root required) |

---

## Project Structure

```
SysPilot/
├── config/
│   ├── syspilot.service    # Systemd service configuration
│   └── syspilot.timer      # Systemd timer (runs every 5 minutes)
├── sys/
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Orchestrator with concurrent execution
│   ├── cpu.py              # CPU usage & temperature monitoring
│   ├── ram.py              # RAM & SWAP memory monitoring
│   ├── disk.py             # Disk space monitoring
│   ├── temperatures.py     # Hardware sensor monitoring
│   └── battery.py          # Battery health tracking (laptop only)
├── requirements.txt        # Python dependencies
├── LICENSE.md              # MIT License
└── README.md               # This file
```

**Highlights:**

- Modular and fault-isolated design
- Concurrent execution via `ThreadPoolExecutor`
- Logs for each component (CPU, RAM, Disk, Battery, etc.)
- Safe to run under **systemd user** (no root access needed)

---

### Architectural Design

**Example: Concurrent Execution Pattern**

```python
    with ThreadPoolExecutor(max_workers=len(MODULES)) as executer:
        futures = [executer.submit(run_Modules, m) for m in MODULES]
        for _ in futures:
            pass

```

---

## Installation & Setup

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip libnotify-bin zenity upower

# Fedora/RHEL
sudo dnf install python3 python3-pip libnotify zenity upower

# Arch Linux
sudo pacman -S python python-pip libnotify zenity upower
```

### Installation Steps

1. **Clone Repository**

```bash
git clone https://github.com/krushangptl/syspilot.git
cd syspilot
```

2. **Install Python Dependencies**

```bash
pip install -r requirements.txt
```

3. **Test Individual Modules**

```bash
cd sys
python3 cpu.py
python3 ram.py
python3 disk.py
python3 temperatures.py
python3 battery.py  # Skip on desktop systems without battery
```

4. **Verify Main Orchestrator**

```bash
python3 main.py
# Check logs
ls -lh ~/.Monitor/
tail -f ~/.Monitor/*.log
```

5. **Run Automaticallu User Space Systemd Service**

```bash
# Update the path in service file
vim config/syspilot.service
# Change: ExecStart=/usr/bin/python3 /absolute/path/to/syspilot/sys/main.py

mkdir -p ~/.config/systemd/user/

# Install service and timer in user space
sudo cp config/syspilot.service ~/.config/systemd/user/
sudo cp config/syspilot.timer ~/.config/systemd/user/
sudo systemctl daemon-reload

# Enable and start timer
systemctl --user enable syspilot.timer
systemctl --user start syspilot.timer

# Verify installation
systemctl --user list-timers --all
systemctl --user status syspilot.timer
systemctl --user list-timers --all | grep syspilot
systemctl --user status syspilot.service

```

6. **Monitor Daemon Activity**

```bash
# View monitoring logs
tail -f ~/.Monitor/*.log
```

---

## Configuration

### Customizing Alert Thresholds

Edit the respective module files in `sys/` directory:

**sys/cpu.py**

```python
ALERT_CPU_THRESHOLD = 90      # % usage (0-100)
ALERT_TEMP_THRESHOLD = 85     # Celsius
AVG_WINDOW = 5                # Rolling average window size
```

**sys/ram.py**

```python
ALERT_RAM_THRESHOLD = 85      # % usage (0-100)
ALERT_SWAP_THRESHOLD = 70     # % usage (0-100)
```

**sys/disk.py**

```python
ALERT_DISK_THRESHOLD = 85     # % usage (0-100)
```

**sys/temperatures.py**

```python
ALERT_TEMP_THRESHOLD = 85     # Celsius
```

**sys/battery.py**

```python
# Low battery warning threshold (line 77)
if battery["percentage"] < 20 and battery.get("state") == "discharging":

# High battery warning threshold (line 83)
if battery["percentage"] > 80 and battery.get("state") == "charging":
```

### Adjusting Monitoring Interval

Edit `config/syspilot.timer`:

```ini
[Timer]
OnBootSec=1min           # Delay after system boot
OnUnitActiveSec=5min     # Run every 5 minutes (adjust as needed)
Persistent=true          # Catch up on missed runs after downtime
```

Common intervals:

- `1min` - High-frequency monitoring (higher CPU usage)
- `5min` - Recommended for balanced monitoring
- `15min` - Low-frequency monitoring (minimal resource usage)

### Notification Customization

**Disable Audio Alerts:**
Comment out sound playback in modules:

```python
# subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"])
```

**Change Notification Style:**

- `sys/cpu.py`, `sys/ram.py`: Use `notify-send` (lightweight)
- `sys/temperatures.py`, `sys/battery.py`: Use `zenity` (modal dialogs)

---

## Log Files & Output

All monitoring logs are stored in `~/.Monitor/`:

```
~/.Monitor/
├── cpu_usage.log          # CPU metrics and core temperatures
├── ram_usage.log          # RAM and SWAP usage statistics
├── disk_usage.log         # Per-partition disk space usage
├── temperatures.log       # All hardware sensor readings
├── battery_health.log     # Battery health tracking (laptops only)
└── Monitor.log            # Daemon error logs (from main.py)
```

---

## Tesing and Validation

I'm still learning fromal testing, so for now all features were **manually validated** by:

- Running each module individually
- Simulating high CPU load, low memory and disk full conditions
- Verifying alerts and log output
- Confirming graceful handling of missing hardware

**Future Plan:**

- Add unit tests and mock system metrics
- Automate validation through simulated resource thresholds

---

## Troubleshooting

| Issue                         | Fix                                                  |
| ----------------------------- | ---------------------------------------------------- |
| **No notifications**          | Check if `dunst` or `notification-daemon` is running |
| **Battery errors on desktop** | Expected behavior (no hardware present)              |
| **Logs missing**              | Ensure `~/.Monitor` exists and is writable           |
| **High CPU usage**            | Increase `OnUnitActiveSec` interval in timer file    |

---

---

## Future Enhancements

### Planned Features

- [ ] **Network Monitoring** - Bandwidth usage and active connections
- [ ] **Process Monitor** - Track top resource-consuming processes
- [ ] **GPU Monitoring** - NVIDIA/AMD GPU usage and temperature (for gaming/ML rigs)
- [ ] **Historical Charts** - Generate usage graphs from logs
- [ ] **Configuration File** - YAML/TOML config instead of hardcoded thresholds

---

## Tech Stack

- **Language**: Python3
- **Libraries**: `psutil`, `concurrent.futures`
- **Platform**: Linux (Ubuntu in my case)
- **Integration**: systemd (user service)
- **Concepts**: Daemon desing, concurrency, fault tolerance, system monitoring

---

## About

Through this project I learnd:

- How **systemd user daemon** work
- How to desing **modular concurrent applications**
- How to **monitor Linux resources programmatically**

If you have suggestions, feedback or ideas, feel free to open an issue or PR!

🌟 [Star the repo](https://github.com/krushangptl/syspilot) if you find it useful.

---

## Summary

**SysPilot** — a modular Linux daemon that monitors system resources and sends desktop alerts.  
Built using Python, psutil, and systemd (user services).  
Demonstrates Linux system programming, concurrent execution, error handling, and automation skills.
