import pytest

from clipbridge.app import app as clipbridge_app


@pytest.fixture
def app(monkeypatch):
    """Configure the Flask app for an isolated test request."""
    monkeypatch.setitem(clipbridge_app.config, "TESTING", True)
    monkeypatch.setitem(clipbridge_app.config, "AUTH_TOKEN", None)
    monkeypatch.setitem(clipbridge_app.config, "MAX_CONTENT_LENGTH", 1024)
    return clipbridge_app
