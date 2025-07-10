# LLM Notify MCP

Local notification bridge for LLM agents. Send immediate audio and visual notifications to developers during long-running AI-assisted tasks.

🎯 **Available as both standalone server and MCP (Model Context Protocol) server for seamless Claude Desktop integration.**

## Quick Start

### 🚀 MCP Server (Recommended for Claude Desktop)

**For Claude Desktop integration** (enables Claude to send you notifications):

1. **Configure**: Add to Claude Desktop config (see [MCP_SETUP.md](MCP_SETUP.md)) - uses `uvx` (no installation needed!)
2. **Use**: Ask Claude to notify you! *"Claude, let me know when you're done with this analysis."*

> ✨ **No manual installation required** - `uvx` automatically handles the package for you!

### 📦 Standalone Installation

```bash
# Install with uv (recommended)
uv pip install llm-notify-mcp

# Or with pip
pip install llm-notify-mcp
```

### Demo

```bash
# Test that everything works
llm-notify-mcp --demo
```

You should hear "LLM Notify MCP is ready" spoken aloud.

### Basic Usage

```python
from llm_notify_mcp import notify

# Simple notification
notify("Model training complete!")

# With priority
notify("Critical error occurred!", priority="high")

# With source identifier
notify("Database backup finished", source="backup-agent")
```

### Start the Server

```bash
# Start server (foreground)
llm-notify-mcp

# Start server in background
llm-notify-mcp --start-daemon

# Custom host/port
llm-notify-mcp --host 127.0.0.1 --port 8765
```

## Configuration

LLM Notify MCP uses a YAML configuration file located at `~/.llm-notify-mcp/config.yaml`.

Create a default config:

```bash
llm-notify-mcp --create-config
```

Example configuration:

```yaml
# Server settings
host: "127.0.0.1"
port: 8765

# Audio settings
voice: ""  # Empty uses system default voice (recommended)
volume: 0.8
speech_rate: 180

# Notification settings
visual_notifications: true
rate_limit: 10  # messages per minute

# Security (optional)
auth_token: "your-secret-token"

# Logging
log_level: "INFO"
```

## API Usage

### REST API

```bash
# Send notification
curl -X POST http://localhost:8765/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Task completed", "priority": "normal"}'

# With authentication
curl -X POST http://localhost:8765/notify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{"message": "Task completed", "priority": "normal"}'

# Health check
curl http://localhost:8765/health
```

### Python SDK

```python
from llm_notify_mcp import notify, configure_client

# Configure client (optional)
configure_client(host="127.0.0.1", port=8765, auth_token="your-token")

# Send notifications
notify("Training complete!")
notify("Error occurred!", priority="high")

# Async usage
import asyncio
from llm_notify_mcp import notify_async

async def main():
    await notify_async("Async notification")

asyncio.run(main())
```

## Integration Examples

### OpenAI Assistant

```python
import openai
from llm_notify_mcp import notify

def run_assistant_task():
    try:
        # Your OpenAI assistant code here
        response = openai.ChatCompletion.create(...)
        
        notify("Assistant task completed successfully!")
        return response
    except Exception as e:
        notify(f"Assistant task failed: {str(e)[:100]}", priority="high")
        raise
```

### Long-running ML Training

```python
import tensorflow as tf
from llm_notify_mcp import notify

def train_model():
    try:
        # Model training code
        model = tf.keras.Sequential([...])
        model.compile(...)
        
        notify("Starting model training...")
        
        history = model.fit(...)
        
        notify(f"Training complete! Final accuracy: {history.history['accuracy'][-1]:.3f}")
        
    except Exception as e:
        notify(f"Training failed: {str(e)[:100]}", priority="high")
```

## Security

- **Local-only**: All communication happens on localhost (127.0.0.1)
- **No persistence**: Messages are not stored after delivery
- **Optional authentication**: Bearer token support for additional security
- **Rate limiting**: Prevents message spam (configurable)

## Requirements

- **Python**: 3.12+
- **macOS**: Required for text-to-speech functionality
- **Audio**: macOS `say` command (built-in)
- **Visual**: macOS notification system (optional)

> 💡 **Voice Quality Tip**: For much better voice quality, see [VOICE_GUIDE.md](VOICE_GUIDE.md) for instructions on downloading enhanced voices from System Settings.

## License

MIT License - see LICENSE file for details.