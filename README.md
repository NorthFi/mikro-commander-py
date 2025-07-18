# /README.md example as follow # mikro-commander-py/README.md
```
# Mikro Commander Py

**Multi-device SSH command runner for MikroTik RouterOS**

---

## Features

- Run multiple RouterOS commands on multiple MikroTik devices via SSH
- Tabbed GUI for commands, targets, output, and settings
- Threaded execution for fast batch operations
- Input validation, per-device logging, config persistence
- Modular, testable codebase

---

## Installation

```bash
git clone https://github.com/NorthFi/mikro-commander-py.git
cd mikro-commander-py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or install via Poetry (if you prefer):

```bash
poetry install
```

---

## Usage

```bash
python main.py
```

- Enter commands in the "Commands" tab (one per line)
- Enter target device IPs in the "Targets" tab (one per line or load from file)
- Set SSH credentials and options in "Settings"
- View output and logs in the "Output" tab
- Click **Execute** to run commands on all devices

---

## Project Structure

```
mikro-commander-py/
├── core/       # SSH, config, logging, controller modules
├── gui/        # GUI tabs and integration
├── utils/      # Validation and file helpers
├── tests/      # Pytest test suite
├── main.py     # Application entrypoint
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Running Tests

```bash
pytest tests/
```

---

## Contributing

- Fork the repo and submit PRs for bugfixes or enhancements!
- Please add tests for new functionality.
- For major changes, open an issue first.

---

## License

MIT
```
