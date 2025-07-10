"""MCP server implementation for LLM Notify MCP."""

import asyncio
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent

from .config import Config
from .server import NotificationServer, NotificationRequest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("LLM Notify MCP")

# Global notification server instance
_notification_server: NotificationServer | None = None


def get_notification_server() -> NotificationServer:
    """Get or create the notification server instance."""
    global _notification_server
    if _notification_server is None:
        config = Config.load()
        _notification_server = NotificationServer(config)
    return _notification_server


@mcp.tool()
async def notify(
    message: str,
    priority: str = "normal",
    source: str | None = None
) -> str:
    """
    Send a notification to the user via text-to-speech and visual notification.
    
    Args:
        message: The message to speak and display (max 140 characters)
        priority: Priority level - "low", "normal", or "high" (default: "normal")
        source: Optional source identifier for the notification
    
    Returns:
        Success message or error details
    """
    try:
        # Validate message length
        if len(message) > 140:
            return f"Error: Message too long ({len(message)} chars). Maximum 140 characters allowed."
        
        # Validate priority
        if priority not in ["low", "normal", "high"]:
            return f"Error: Invalid priority '{priority}'. Must be 'low', 'normal', or 'high'."
        
        # Create notification request
        request = NotificationRequest(
            message=message,
            priority=priority,
            source=source
        )
        
        # Send notification
        server = get_notification_server()
        await server._send_notification(request)
        
        return f"Notification sent successfully: '{message}'"
        
    except Exception as e:
        error_msg = f"Failed to send notification: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
async def test_notification() -> str:
    """
    Send a test notification to verify the system is working.
    
    Returns:
        Success message or error details
    """
    try:
        server = get_notification_server()
        await server.demo()
        return "Test notification sent successfully! You should have heard 'LLM Notify MCP is ready'."
    except Exception as e:
        error_msg = f"Test notification failed: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
async def get_voice_info() -> str:
    """
    Get information about available voices and current configuration.
    
    Returns:
        Voice configuration information
    """
    try:
        config = Config.load()
        
        info = [
            "=== LLM Notify MCP Voice Configuration ===",
            f"Current voice: {'System default' if not config.voice else config.voice}",
            f"Speech rate: {config.speech_rate} words per minute",
            f"Visual notifications: {'Enabled' if config.visual_notifications else 'Disabled'}",
            "",
            "💡 For better voice quality:",
            "1. Open System Settings > Accessibility > Spoken Content",
            "2. Click the ℹ️ next to 'System voice'", 
            "3. Download Enhanced/Premium voices (Ava, Evan, Zoe, etc.)",
            "",
            "📝 To customize: Edit ~/.llm-notify-mcp/config.yaml",
            "🎵 Test voices: Use 'test_notification' tool"
        ]
        
        return "\n".join(info)
        
    except Exception as e:
        error_msg = f"Failed to get voice info: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
async def configure_notifications(
    voice: str = "",
    speech_rate: int = 180,
    visual_notifications: bool = True
) -> str:
    """
    Configure notification settings.
    
    Args:
        voice: Voice name (empty string for system default)
        speech_rate: Speech rate in words per minute (recommended: 150-200)
        visual_notifications: Whether to show visual notifications
    
    Returns:
        Configuration update status
    """
    try:
        config = Config.load()
        
        # Update configuration
        config.voice = voice
        config.speech_rate = speech_rate
        config.visual_notifications = visual_notifications
        
        # Save configuration
        config.save()
        
        # Update global server instance
        global _notification_server
        _notification_server = NotificationServer(config)
        
        voice_desc = "System default" if not voice else voice
        return (
            f"Configuration updated successfully:\n"
            f"- Voice: {voice_desc}\n"
            f"- Speech rate: {speech_rate} WPM\n"
            f"- Visual notifications: {'Enabled' if visual_notifications else 'Disabled'}\n"
            f"Use 'test_notification' to try the new settings."
        )
        
    except Exception as e:
        error_msg = f"Failed to configure notifications: {str(e)}"
        logger.error(error_msg)
        return error_msg


def main():
    """Main entry point for the MCP server."""
    import sys
    
    # Log startup
    logger.info("Starting LLM Notify MCP server...")
    
    try:
        # Initialize notification server to validate configuration
        get_notification_server()
        logger.info("Notification server initialized successfully")
        
        # Run the MCP server
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()