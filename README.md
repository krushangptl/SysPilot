# SysPilot

**A lightweight Linux system monitoring daemon for minimalist desktops.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)

---

## Overview

SysPilot is a modular, fault-tolerant daemon that monitors key system resources — CPU, RAM, disk, temperature,
and battery — and triggers desktop notifications when predefined thresholds are reached.

Designed for **minimal Linux environments** (i3wm, Sway, bspwm) where GUI monitoring tools are absent.
Runs as a **systemd user service** without root privileges.

---

## Core Features

| Component                | Description                                           |
| ------------------------ | ----------------------------------------------------- |
| CPU / Temp Monitoring    | Tracks usage and temperature with configurable alerts |
| Memory / Swap Monitoring | Monitors RAM and SWAP utilization                     |
| Disk Monitoring          | Multi-partition disk usage alerts                     |
| Battery Health           | Tracks charge %, state, and capacity degradation      |
| Notifications            | `notify-send` / `zenity` for critical events          |
| Logging                  | Detailed per-component logs in `~/.Monitor/`          |
| Systemd Integration      | Runs automatically via user service and timer         |

---

## Architecture

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
└── README.md               # READEM
```

**Concurrency Pattern:**

```python
with ThreadPoolExecutor(max_workers=len(MODULES)) as executor:
    futures = [executor.submit(run_module, m) for m in MODULES]
    for _ in futures:
        pass

```

- Each module executes independently, logs metrics, and raises alerts without bloging others.
- Modular design allows easy extension (network, process, GPU monitoring).

---

## Future Enhancements

**Planned Features**

- [ ] **Network Monitoring** - Bandwidth usage and active connections
- [ ] **Process Monitor** - Track top resource-consuming processes
- [ ] **Historical Charts** - Generate usage graphs from logs
- [ ] **Configuration File** - YAML/TOML config instead of hardcoded

---

## Tech Stack

- **Language**: Python3
- **Libraries**: `psutil`, `concurren.futures` and builtin libs
- **Platform**: Linux (tested on Ubuntu 22.04 LTS)
- **Concepts**: Daemon Desigin, concurrency, systemd integration, fault-tolerant

---

### Next Steps

- For installation, configuration, and systemd setup see [SETUP.md](/docs/SETUP.md)
- For contributing and submitting improvement see [CONTRIBUTION-GUIDE.md](/docs/CONTRIBUTION-GUIDE.md)
