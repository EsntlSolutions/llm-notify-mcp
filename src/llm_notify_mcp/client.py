"""LLM Notify MCP client SDK."""

import asyncio
import logging

import aiohttp

logger = logging.getLogger(__name__)


class NotificationClient:
    """Client for sending notifications to LLM Notify MCP server."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        auth_token: str | None = None,
        timeout: float = 5.0
    ):
        self.base_url = f"http://{host}:{port}"
        self.auth_token = auth_token
        self.timeout = timeout

    async def send_notification(
        self,
        message: str,
        priority: str = "normal",
        source: str | None = None
    ) -> bool:
        """Send a notification to the server."""

        if len(message) > 140:
            raise ValueError("Message must be 140 characters or less")

        payload = {
            "message": message,
            "priority": priority,
        }

        if source:
            payload["source"] = source

        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f"{self.base_url}/notify",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return True
                    elif response.status == 429:
                        logger.warning("Rate limit exceeded")
                        return False
                    else:
                        logger.error(f"Notification failed: {response.status}")
                        return False

        except TimeoutError:
            logger.error("Notification timed out")
            return False
        except Exception as e:
            logger.error(f"Notification failed: {e}")
            return False

    async def health_check(self) -> bool:
        """Check if the server is healthy."""
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{self.base_url}/health") as response:
                    return response.status == 200
        except Exception:
            return False


# Global client instance
_client: NotificationClient | None = None


def configure_client(
    host: str = "127.0.0.1",
    port: int = 8765,
    auth_token: str | None = None,
    timeout: float = 5.0
):
    """Configure the global notification client."""
    global _client
    _client = NotificationClient(host, port, auth_token, timeout)


def get_client() -> NotificationClient:
    """Get the global notification client."""
    global _client
    if _client is None:
        _client = NotificationClient()
    return _client


def notify(
    message: str,
    priority: str = "normal",
    source: str | None = None,
    fallback_print: bool = True
) -> bool:
    """Send a notification (synchronous wrapper)."""

    if len(message) > 140:
        if fallback_print:
            msg_len = len(message)
            print(f"Warning: Message too long ({msg_len} chars), truncating to 140")
        message = message[:140]

    try:
        client = get_client()

        # Run async function in event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        success = loop.run_until_complete(
            client.send_notification(message, priority, source)
        )

        if not success and fallback_print:
            print(f"[LLM Notify MCP] {message}")

        return success

    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        if fallback_print:
            print(f"[LLM Notify MCP] {message}")
        return False


async def notify_async(
    message: str,
    priority: str = "normal",
    source: str | None = None
) -> bool:
    """Send a notification (async)."""

    if len(message) > 140:
        message = message[:140]

    client = get_client()
    return await client.send_notification(message, priority, source)
