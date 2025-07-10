# MCP Server Setup Guide

## 🚀 Quick Setup for Claude Desktop

### 1. Ensure uvx is Available
```bash
# uvx comes with uv - install if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

**Note**: No need to install llm-notify-mcp manually - `uvx` will handle it automatically!

### 2. Add to Claude Desktop Configuration

**On macOS:** Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**On Windows:** Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

**If installed from PyPI (after publication):**
```json
{
  "mcpServers": {
    "llm-notify-mcp": {
      "command": "uvx",
      "args": ["llm-notify-mcp", "--mcp-server"],
      "env": {}
    }
  }
}
```

**For local development/testing:**
```json
{
  "mcpServers": {
    "llm-notify-mcp": {
      "command": "uvx",
      "args": ["--from", "/path/to/llm-notify-mcp", "llm-notify-mcp", "--mcp-server"],
      "env": {}
    }
  }
}
```

**From Git repository:**
```json
{
  "mcpServers": {
    "llm-notify-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/yourusername/llm-notify-mcp.git", "llm-notify-mcp", "--mcp-server"],
      "env": {}
    }
  }
}
```

### 3. Restart Claude Desktop

After adding the configuration, restart Claude Desktop to load the MCP server.

## 🎯 Available Tools

Once configured, Claude will have access to these notification tools:

### `notify`
Send a notification with text-to-speech and visual alert.

**Parameters:**
- `message` (required): The message to speak (max 140 characters)
- `priority` (optional): "low", "normal", or "high" (default: "normal")  
- `source` (optional): Source identifier for the notification

**Example:**
```
Claude, please notify me when you're done: "Analysis complete!"
```

### `test_notification`
Send a test notification to verify everything is working.

**Example:**
```
Claude, send a test notification to make sure the system is working.
```

### `get_voice_info`
Get information about current voice configuration and setup tips.

**Example:**
```
Claude, show me the current voice configuration.
```

### `configure_notifications`
Update notification settings.

**Parameters:**
- `voice` (optional): Voice name or empty for system default
- `speech_rate` (optional): Words per minute (recommended: 150-200)
- `visual_notifications` (optional): Enable/disable visual notifications

**Example:**
```
Claude, configure notifications to use a slower speech rate of 150 WPM.
```

## 🎵 Voice Quality Setup

For the best voice quality:

1. **Open System Settings > Accessibility > Spoken Content**
2. **Click the ℹ️ next to "System voice"**
3. **Download Enhanced/Premium voices** like:
   - Ava (Enhanced/Premium)
   - Evan (Enhanced/Premium)
   - Zoe (Enhanced/Premium)

## 🔧 Configuration

The MCP server uses the same configuration as the standalone version:

**Config file location:** `~/.llm-notify-mcp/config.yaml`

**Example configuration:**
```yaml
# Audio settings
voice: ""          # Empty uses system default (recommended)
volume: 0.8
speech_rate: 180

# Notification settings  
visual_notifications: true
rate_limit: 10

# Security (optional)
auth_token: ""

# Logging
log_level: "INFO"
```

## 🧪 Testing

### Test from Command Line
```bash
# Test the MCP server directly (via uvx)
uvx llm-notify-mcp --mcp-server

# Test the notification system
uvx llm-notify-mcp --demo
```

### Test with Claude
Once configured in Claude Desktop, try:

```
Claude, send me a test notification to make sure everything is working.
```

You should hear "LLM Notify MCP is ready" spoken aloud and see a visual notification.

## 🎯 Usage Examples

### Basic Notifications
```
Claude, notify me: "Code compilation finished successfully"

Claude, send me a high priority alert: "System backup failed"

Claude, let me know when you're done with the analysis.
```

### Long-Running Tasks
```
Claude, analyze this large dataset and notify me when complete.

Claude, summarize these 50 documents and alert me when finished.

Claude, help me debug this code and notify me if you find the issue.
```

### Configuration Management
```
Claude, what's my current voice configuration?

Claude, set the speech rate to 160 WPM for clearer speech.

Claude, disable visual notifications and keep only audio.
```

## 🐛 Troubleshooting

### MCP Server Not Loading
1. Check that `llm-notify-mcp-server` command is in your PATH
2. Verify the JSON configuration is valid
3. Restart Claude Desktop after configuration changes
4. Check Claude Desktop's console for error messages

### Audio Not Working
1. Test with: `llm-notify-mcp --demo`
2. Check System Settings > Sound > Output Device
3. Try different voices with `get_voice_info` tool
4. Verify audio permissions for the terminal/Claude

### Visual Notifications Not Showing
1. Check System Settings > Notifications > Allow notifications
2. Set `visual_notifications: true` in config
3. Test with the `test_notification` tool

## 🎉 Integration Examples

### Research Assistant
```
Claude, search through these research papers for mentions of "machine learning bias" and notify me with a summary when done.
```

### Code Analysis
```
Claude, review this codebase for security vulnerabilities and alert me with your findings.
```

### Data Processing
```
Claude, process this CSV file and calculate statistics, then notify me with the results.
```

The MCP integration makes LLM Notify MCP seamlessly available to Claude for any task where you want to be notified of completion or important updates!