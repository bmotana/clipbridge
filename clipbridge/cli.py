"""Command-line entry point for the Clipbridge server."""

from clipbridge.app import app


def main():
    """Run the HTTP server."""
    # host='0.0.0.0' allows external devices on the local network to connect.
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
