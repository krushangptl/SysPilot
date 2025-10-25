# Contributing to SysPilot

Welcome! This guide explains how to contribute code, report issues, and submit pull requests.

---

## 1. Reporting Issues

- Use GitHub Issues for bug reports or feature requests.
- Provide clear description, OS, Python version, and logs if applicable.

---

## 2. Code Contributions

### Steps:

1. Fork the repository
2. Clone your fork

```bash
git clone https://github.com/<your-username>/syspilot.git
```

3. Create a feature branch

```bash
git checkout -b feature/<name>
```

4. Make your changes following existing code structure
5. Run local tests

**Commit Guidelines**

- Use descriptive commit messages

```text
Fix(cpu): handle missing sensors gracefully
Add(logging): create per-module log file if missing
```

---

## 3. Pull Requests

1. Push your branch

```bash
git push origin feature/<name>
```

2. Open PR against `master` branch
3. Link related issues
4. Ensure PR passed CI/Lintig (if added)
5. Respond to review comments promptly

---

## 4. Code Standards

- Maintain modular structure (`sys/*.py`)
- Use `ThreadPoolExecutor` pattern for concurrent modules
- Log all critical events
- Document new function and modules

---
