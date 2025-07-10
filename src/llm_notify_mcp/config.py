"""Configuration management for LLM Notify MCP."""

from pathlib import Path

import yaml
from pydantic import BaseModel


class Config(BaseModel):
    """Configuration model for LLM Notify MCP."""

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8765

    # Audio settings
    voice: str = ""  # Empty string uses system default voice
    volume: float = 0.8
    speech_rate: int = 180  # words per minute

    # Notification settings
    visual_notifications: bool = True
    rate_limit: int = 10  # messages per minute

    # Security settings
    auth_token: str | None = None

    # Logging settings
    log_level: str = "INFO"

    @classmethod
    def load(cls, config_path: Path | None = None) -> "Config":
        """Load configuration from file or use defaults."""

        if config_path is None:
            config_path = Path.home() / ".llm-notify-mcp" / "config.yaml"

        if config_path.exists():
            try:
                with open(config_path) as f:
                    config_data = yaml.safe_load(f)
                return cls(**config_data)
            except Exception as e:
                print(f"Warning: Failed to load config from {config_path}: {e}")
                print("Using default configuration")

        return cls()

    def save(self, config_path: Path | None = None):
        """Save configuration to file."""

        if config_path is None:
            config_path = Path.home() / ".llm-notify-mcp" / "config.yaml"

        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(config_path, "w") as f:
                yaml.safe_dump(self.model_dump(), f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Failed to save config to {config_path}: {e}")

    def get_config_dir(self) -> Path:
        """Get the configuration directory."""
        return Path.home() / ".llm-notify-mcp"

    def get_log_dir(self) -> Path:
        """Get the log directory."""
        return self.get_config_dir() / "logs"
