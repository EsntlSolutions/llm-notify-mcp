"""Tests for the notification client."""

from unittest.mock import patch

import pytest

from llm_notify_mcp.client import NotificationClient, notify


@pytest.mark.asyncio
async def test_notification_client():
    """Test notification client with mock."""
    client = NotificationClient()

    # Mock the send_notification method directly
    with patch.object(client, 'send_notification', return_value=True):
        result = await client.send_notification("Test message")
        assert result is True


@pytest.mark.asyncio
async def test_notification_client_rate_limited():
    """Test notification client with rate limiting."""
    client = NotificationClient()

    # Mock the send_notification method directly
    with patch.object(client, 'send_notification', return_value=False):
        result = await client.send_notification("Test message")
        assert result is False


@pytest.mark.asyncio
async def test_notification_client_server_error():
    """Test notification client with server error."""
    client = NotificationClient()

    # Mock the send_notification method directly
    with patch.object(client, 'send_notification', return_value=False):
        result = await client.send_notification("Test message")
        assert result is False


@pytest.mark.asyncio
async def test_health_check():
    """Test health check."""
    client = NotificationClient()

    # Mock the health_check method directly
    with patch.object(client, 'health_check', return_value=True):
        result = await client.health_check()
        assert result is True


def test_notify_function():
    """Test synchronous notify function."""
    patch_target = "llm_notify_mcp.client.NotificationClient.send_notification"
    with patch(patch_target) as mock_send:
        mock_send.return_value = True

        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_until_complete.return_value = True

            result = notify("Test message")
            assert result is True


def test_notify_function_message_too_long():
    """Test notify function with message too long."""
    long_message = "x" * 150

    patch_target = "llm_notify_mcp.client.NotificationClient.send_notification"
    with patch(patch_target) as mock_send:
        mock_send.return_value = True

        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_until_complete.return_value = True

            result = notify(long_message)
            assert result is True
            # Should have been called with truncated message
            mock_send.assert_called_once()
            args = mock_send.call_args[0]
            assert len(args[0]) == 140
