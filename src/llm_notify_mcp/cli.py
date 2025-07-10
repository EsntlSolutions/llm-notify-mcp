"""Command-line interface for LLM Notify MCP."""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

import uvicorn

from .config import Config
from .server import NotificationServer


def setup_logging(config: Config):
    """Set up logging configuration."""

    log_dir = config.get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "mcp-notify.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


async def run_demo(config: Config):
    """Run a demonstration notification."""
    server = NotificationServer(config)
    try:
        await server.demo()
        print("Demo notification sent successfully!")
    except Exception as e:
        print(f"Demo failed: {e}")
        sys.exit(1)


def start_server(config: Config, daemon: bool = False):
    """Start the notification server."""

    setup_logging(config)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting LLM Notify MCP server on {config.host}:{config.port}")

    server = NotificationServer(config)

    uvicorn_config = {
        "app": server.app,
        "host": config.host,
        "port": config.port,
        "log_config": None,  # Use our own logging
        "access_log": False,
    }

    if daemon:
        # For daemon mode, we might want to add additional setup
        # like pid file management, but for now just run normally
        pass

    try:
        uvicorn.run(**uvicorn_config)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed: {e}")
        sys.exit(1)


def create_config_template():
    """Create a default configuration file."""
    config = Config()
    config_path = config.get_config_dir() / "config.yaml"

    if config_path.exists():
        print(f"Configuration file already exists at {config_path}")
        return

    config.save(config_path)
    print(f"Created default configuration at {config_path}")


def main():
    """Main CLI entry point."""

    parser = argparse.ArgumentParser(
        description="LLM Notify MCP: Local notification bridge for LLM agents"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file"
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Server port (default: 8765)"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a demo notification"
    )

    parser.add_argument(
        "--start-daemon",
        action="store_true",
        help="Start server in daemon mode"
    )

    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Create a default configuration file"
    )

    parser.add_argument(
        "--mcp-server",
        action="store_true",
        help="Run as MCP server for Claude Desktop integration"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="LLM Notify MCP 0.1.0"
    )

    args = parser.parse_args()

    # Handle config creation
    if args.create_config:
        create_config_template()
        return

    # Handle MCP server mode
    if args.mcp_server:
        from .mcp_server import main as mcp_main
        mcp_main()
        return

    # Load configuration
    config = Config.load(args.config)

    # Override config with command line args
    if args.host != "127.0.0.1":
        config.host = args.host
    if args.port != 8765:
        config.port = args.port

    # Handle demo mode
    if args.demo:
        asyncio.run(run_demo(config))
        return

    # Start server
    start_server(config, daemon=args.start_daemon)


if __name__ == "__main__":
    main()
