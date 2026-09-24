import pyperclip
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/clipboard", methods=["POST"])
def update_clipboard():
    # Expecting plain text or JSON payload
    if request.is_json:
        data = request.get_json()
        print(data)
        text = data.get("text", "")
    else:
        text = request.get_data(as_text=True)

    if text:
        pyperclip.copy(text)
        print(f"[+] Clipboard updated: {text[:30]}...")
        return jsonify({"status": "success", "message": "Clipboard updated"}), 200
    else:
        return jsonify({"status": "error", "message": "No text provided"}), 400


if __name__ == "__main__":
    # host='0.0.0.0' allows external devices (like your phone) on the local network to connect
    app.run(host="0.0.0.0", port=5000)
