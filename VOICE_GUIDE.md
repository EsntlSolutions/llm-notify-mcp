# Voice Quality Guide for LLM Notify MCP

## 🎯 Recommended Voices (Best Quality)

### How to Download Enhanced/Premium Voices
For much better voice quality, follow these steps:

1. **Open System Settings > Accessibility > Spoken Content**
2. **Click the ℹ️ (info icon) in the circle next to "System voice"**
3. **Download Enhanced and Premium versions of voices**

**Recommended Enhanced/Premium voices:**
- **Ava (Enhanced/Premium)** - Natural female voice ⭐⭐⭐⭐⭐
- **Evan (Enhanced/Premium)** - Natural male voice ⭐⭐⭐⭐⭐  
- **Zoe (Enhanced/Premium)** - Professional female voice ⭐⭐⭐⭐⭐
- **Nora (Enhanced/Premium)** - Clear female voice ⭐⭐⭐⭐⭐
- **Nathan (Enhanced/Premium)** - Professional male voice ⭐⭐⭐⭐⭐

### Built-in Voices (Available Now)
**Default:**
- **System Default Voice** (current default) - Uses whatever voice is set in System Settings ⭐⭐⭐⭐

**Other Built-in Options:**
- **Samantha** - Clear female voice ⭐⭐⭐
- **Fred** - Classic male voice ⭐⭐⭐
- **Kathy** - Clear female voice ⭐⭐⭐

**Acceptable Quality:**
- **Albert** - Professional male voice ⭐⭐
- **Ralph** - Deep male voice ⭐⭐

**Fun/Novelty Voices:**
- **Good News** - Upbeat/excited voice
- **Bad News** - Somber voice
- **Whisper** - Quiet voice

## 🔧 How to Change Voice

### Method 1: Configuration File
Edit `~/.llm-notify-mcp/config.yaml`:
```yaml
voice: ""          # Uses system default (recommended)
voice: "Samantha"  # Or specify a specific voice name
```

### Method 2: Test Voices
```bash
# Test different voices
say -v Samantha "Testing voice quality"
say -v Fred "Testing voice quality"
say -v Kathy "Testing voice quality"
```

## 🚀 Future Improvements

We're considering adding support for:
- **espeak-ng** (better open-source TTS)
- **Cloud TTS services** (AWS Polly, Google, Azure)
- **Custom voice training**

## 📋 Available Voices on Your System

Run this command to see all available voices:
```bash
say -v '?' | grep en_US
```

## 💡 Tips

1. **Download Enhanced Voices**: The built-in voices are basic. Enhanced voices sound much more natural.
2. **Test Before Configuring**: Use `say -v VoiceName "test"` to hear each voice
3. **Consider Context**: Some voices work better for alerts vs. longer messages
4. **Rate Adjustment**: Slower rates often sound more natural:
   - **150-170**: Very natural, easy to understand
   - **180**: Good balance (current default)
   - **200+**: Fast, good for urgent alerts
   - **100-140**: Slow, good for detailed information

### Test Different Speech Rates
```bash
say -r 150 "Testing slow speech rate"
say -r 180 "Testing normal speech rate" 
say -r 220 "Testing fast speech rate"
```