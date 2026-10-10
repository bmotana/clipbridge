from unittest.mock import Mock

import pyperclip
import pytest


@pytest.fixture
def clipboard_copy(monkeypatch):
    copy = Mock()
    monkeypatch.setattr(pyperclip, "copy", copy)
    return copy


def test_accepts_json_text(client, clipboard_copy):
    response = client.post("/clipboard", json={"text": "JSON clipboard text"})

    assert response.status_code == 200
    assert response.get_json()["status"] == "success"
    clipboard_copy.assert_called_once_with("JSON clipboard text")


def test_accepts_plain_text(client, clipboard_copy):
    response = client.post(
        "/clipboard", data="plain clipboard text", content_type="text/plain"
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "success"
    clipboard_copy.assert_called_once_with("plain clipboard text")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"json": {}},
        {"json": {"text": ""}},
        {"data": "", "content_type": "text/plain"},
    ],
)
def test_missing_or_empty_text_returns_400(client, clipboard_copy, kwargs):
    response = client.post("/clipboard", **kwargs)

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"
    clipboard_copy.assert_not_called()


def test_rejects_request_without_authentication(client, app, clipboard_copy):
    app.config["AUTH_TOKEN"] = "test-secret"

    response = client.post("/clipboard", json={"text": "private"})

    assert response.status_code in (401, 403)
    clipboard_copy.assert_not_called()


@pytest.mark.parametrize(
    "headers",
    [
        {"Authorization": "Bearer test-secret"},
        {"X-API-Key": "test-secret"},
    ],
)
def test_accepts_valid_authentication(client, app, clipboard_copy, headers):
    app.config["AUTH_TOKEN"] = "test-secret"

    response = client.post("/clipboard", json={"text": "private"}, headers=headers)

    assert response.status_code == 200
    clipboard_copy.assert_called_once_with("private")


def test_rejects_oversized_request(client, clipboard_copy):
    response = client.post(
        "/clipboard", data="x" * 1025, content_type="text/plain"
    )

    assert response.status_code == 413
    clipboard_copy.assert_not_called()
