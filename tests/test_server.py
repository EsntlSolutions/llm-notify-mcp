"""Tests for the notification server."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from llm_notify_mcp.config import Config
from llm_notify_mcp.server import NotificationServer


@pytest.fixture
def config():
    """Create test configuration."""
    return Config(
        host="127.0.0.1",
        port=8765,
        visual_notifications=False,  # Disable for testing
        rate_limit=100  # High limit for testing
    )


@pytest.fixture
def server(config):
    """Create test server."""
    return NotificationServer(config)


@pytest.fixture
def client(server):
    """Create test client."""
    return TestClient(server.app)


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


@patch("llm_notify_mcp.server.NotificationServer._send_audio_notification")
@patch("llm_notify_mcp.server.NotificationServer._send_visual_notification")
def test_notify_endpoint(mock_visual, mock_audio, client):
    """Test notification endpoint."""
    mock_audio.return_value = None
    mock_visual.return_value = None

    response = client.post("/notify", json={
        "message": "Test notification",
        "priority": "normal"
    })

    if response.status_code != 200:
        print(f"Response: {response.status_code}, {response.text}")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "timestamp" in data


def test_notify_message_too_long(client):
    """Test notification with message too long."""
    long_message = "x" * 141  # 141 characters

    response = client.post("/notify", json={
        "message": long_message,
        "priority": "normal"
    })

    assert response.status_code == 422  # Validation error


def test_notify_empty_message(client):
    """Test notification with empty message."""
    response = client.post("/notify", json={
        "message": "",
        "priority": "normal"
    })

    assert response.status_code == 422  # Validation error


def test_notify_invalid_priority(client):
    """Test notification with invalid priority."""
    response = client.post("/notify", json={
        "message": "Test message",
        "priority": "invalid"
    })

    assert response.status_code == 422  # Validation error


def test_rate_limiting():
    """Test rate limiting functionality."""
    from llm_notify_mcp.server import RateLimiter

    limiter = RateLimiter(max_requests=2, window_seconds=60)

    # First two requests should be allowed
    assert limiter.is_allowed("client1") is True
    assert limiter.is_allowed("client1") is True

    # Third request should be denied
    assert limiter.is_allowed("client1") is False

    # Different client should be allowed
    assert limiter.is_allowed("client2") is True


def test_auth_required():
    """Test authentication when token is required."""
    config = Config(auth_token="secret-token")
    server = NotificationServer(config)
    client = TestClient(server.app)

    # Request without auth should fail
    response = client.post("/notify", json={
        "message": "Test notification",
        "priority": "normal"
    })

    assert response.status_code == 401

    # Request with wrong token should fail
    response = client.post("/notify", json={
        "message": "Test notification",
        "priority": "normal"
    }, headers={"Authorization": "Bearer wrong-token"})

    assert response.status_code == 401


@patch("llm_notify_mcp.server.NotificationServer._send_audio_notification")
def test_auth_valid_token(mock_audio):
    """Test authentication with valid token."""
    mock_audio.return_value = None

    config = Config(auth_token="secret-token")
    server = NotificationServer(config)
    client = TestClient(server.app)

    # Request with correct token should succeed
    response = client.post("/notify", json={
        "message": "Test notification",
        "priority": "normal"
    }, headers={"Authorization": "Bearer secret-token"})

    assert response.status_code == 200
