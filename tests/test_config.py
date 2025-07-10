"""Tests for configuration management."""

import tempfile
from pathlib import Path

from llm_notify_mcp.config import Config


def test_default_config():
    """Test default configuration."""
    config = Config()

    assert config.host == "127.0.0.1"
    assert config.port == 8765
    assert config.voice == ""
    assert config.volume == 0.8
    assert config.visual_notifications is True
    assert config.rate_limit == 10
    assert config.auth_token is None


def test_config_load_nonexistent_file():
    """Test loading config from nonexistent file."""
    config = Config.load(Path("/nonexistent/config.yaml"))

    # Should return defaults
    assert config.host == "127.0.0.1"
    assert config.port == 8765


def test_config_save_and_load():
    """Test saving and loading configuration."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "config.yaml"

        # Create config with custom values
        config = Config(
            host="0.0.0.0",
            port=9999,
            voice="Samantha",
            volume=0.5,
            rate_limit=20,
            auth_token="test-token"
        )

        # Save config
        config.save(config_path)

        # Load config
        loaded_config = Config.load(config_path)

        # Verify values
        assert loaded_config.host == "0.0.0.0"
        assert loaded_config.port == 9999
        assert loaded_config.voice == "Samantha"
        assert loaded_config.volume == 0.5
        assert loaded_config.rate_limit == 20
        assert loaded_config.auth_token == "test-token"


def test_config_directories():
    """Test configuration directory methods."""
    config = Config()

    config_dir = config.get_config_dir()
    log_dir = config.get_log_dir()

    assert config_dir.name == ".llm-notify-mcp"
    assert log_dir.name == "logs"
    assert log_dir.parent == config_dir
