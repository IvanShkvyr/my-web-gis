import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from pathlib import Path

from app.main import app, frontend_dir

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def mock_frontend(tmp_path):
    fake_page = tmp_path / "about.html"
    fake_page.write_text("<h1>About<h1>")

    with patch("app.main.frontend_dir", tmp_path):
        yield tmp_path


def test_existing_page_returns_200(mock_frontend):
    response = client.get("/about.html")
    assert response.status_code == 200


def test_missing_page_returns_404(mock_frontend):
    response = client.get("/nonexistent.html")
    assert response.status_code == 404


def test_dotdot_blocked(mock_frontend):
    response = client.get("/../../../etc/passwd.html")
    assert response.status_code in (400, 404)


def test_slash_in_name_blocked(mock_frontend):
    response = client.get("/subdir/page.html")
    assert response.status_code in (400, 404)


def test_encoded_dotdot_blocked(mock_frontend):
    response = client.get("/..%2F..%2Fetc%2Fpasswd.html")
    assert response.status_code in (400, 404)


def test_backslash_blocked(mock_frontend):
    response = client.get("/..\\..\\etc\\passwd.html")
    assert response.status_code in (400, 404)
