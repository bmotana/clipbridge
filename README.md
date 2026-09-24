# Clipbridge

Clipbridge is a small Flask service that receives text over HTTP and copies it to the clipboard of the machine running the service. It accepts either a JSON request containing a `text` field or a plain-text request body.

## Requirements

- Python 3.10 or newer
- A working clipboard interface on the host machine (required by `pyperclip`)

## Install

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
python clipboard_server.py
```

The server listens on port `5000`. The current configuration binds to `0.0.0.0`, so it can be reachable by other devices on the network. Run it only on a trusted network and use firewall rules as appropriate; this service does not provide authentication or transport encryption.

## Send text

JSON:

```bash
curl -X POST http://localhost:5000/clipboard \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from Clipbridge"}'
```

Plain text:

```bash
curl -X POST http://localhost:5000/clipboard \
  -H "Content-Type: text/plain" \
  --data-binary "Hello from Clipbridge"
```

Successful requests return a JSON status of `success`. Empty request bodies return HTTP `400`.

## Development

Install development tools and run the configured linter:

```bash
python -m pip install -r requirements-dev.txt
ruff check .
```

GitHub Actions runs Ruff on pushes and pull requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
