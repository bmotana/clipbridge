"""HTTP application for updating the host clipboard."""

import hmac
import os

import pyperclip
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
app.config["AUTH_TOKEN"] = os.environ.get("CLIPBRIDGE_AUTH_TOKEN")


@app.before_request
def require_authentication():
    """Require a bearer token or API key when authentication is configured."""
    expected_token = app.config.get("AUTH_TOKEN")
    if not expected_token:
        return None

    authorization = request.headers.get("Authorization", "")
    scheme, _, bearer_token = authorization.partition(" ")
    provided_token = bearer_token if scheme.lower() == "bearer" else ""
    provided_token = request.headers.get("X-API-Key", provided_token)

    if not hmac.compare_digest(provided_token, expected_token):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    return None


@app.route("/clipboard", methods=["POST"])
def update_clipboard():
    # Expecting plain text or JSON payload
    if request.is_json:
        data = request.get_json()
        text = data.get("text", "") if isinstance(data, dict) else ""
    else:
        text = request.get_data(as_text=True)

    if text:
        pyperclip.copy(text)
        print(f"[+] Clipboard updated: {text[:30]}...")
        return jsonify({"status": "success", "message": "Clipboard updated"}), 200
    return jsonify({"status": "error", "message": "No text provided"}), 400
