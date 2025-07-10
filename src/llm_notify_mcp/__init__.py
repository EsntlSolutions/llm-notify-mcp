"""LLM Notify MCP: Local notification bridge for LLM agents."""

from .client import notify
from .server import NotificationServer

__version__ = "0.1.0"
__all__ = ["notify", "NotificationServer"]
