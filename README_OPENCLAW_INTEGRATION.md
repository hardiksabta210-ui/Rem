# 🎙️ REM + OpenClaw: Complete AI Assistant System

**Status:** ✅ Production Ready | **Date:** Feb 21, 2026 | **Version:** 1.0.0

---

## 📌 What is This?

**REM (Remote Engagement Manager)** is a local AI assistant that runs entirely on your machine with no cloud dependencies. It now integrates seamlessly with **OpenClaw**, a multi-channel AI gateway.

### REM Provides:
- 🧠 **LLM** — Text generation using local Ollama (Llama 3.2)
- 🔊 **TTS** — Text-to-speech via GPT-SoVITS (optional)
- 🎤 **ASR** — Speech-to-text using Whisper
- 🌐 **Web Control** — Open YouTube/Google from voice commands
- 💬 **Chat** — Conversation with memory/history
- 🎙️ **Voice Modes** — Always-listening assistant

### OpenClaw Integration:
- 🌉 **HTTP API Bridge** — REM services available via REST
- 🤖 **Agent Support** — Full integration with OpenClaw's AI routing
- 🔌 **Skill Registration** — REM appears as OpenClaw "rem-local" skill
- 🔄 **Bidirectional** — OpenClaw ↔ REM communication

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
```bash
# Ensure you have:
# - Python 3.8+ installed
# - Ollama running: ollama serve (in another terminal)
# - Virtual environment activated: .\.venv\Scripts\Activate.ps1
```

### Run These Commands
```bash
# Navigate to project
cd "C:\Users\hardi\Chat bot\Rem_project"

# Verify services
rem health

# Test LLM
rem llm "What is Python?"

# Test web control
rem web "search youtube for python tutorials"

# Test speech (optional)
rem tts "Hello world"

# Start interactive voice mode
rem voice listen
```

**All of the above should work immediately!**

---

## 📖 Complete Usage Guide

### 1️⃣ Direct REM Commands (Simplest)

No setup required, just use the `rem` command:

```bash
# Text generation
rem llm "Explain quantum computing in simple terms"

# Chat with conversation memory
rem llm-chat "Hello, how are you?"
rem llm-chat "What am I doing?"  # Remembers previous context

# Text to speech (if SoVITS available)
rem tts "The quick brown fox"

# Speech recognition
rem asr "audio/my_voice.wav"

# Web searches
rem web "search youtube for machine learning"
rem web "google what is AI"

# Interactive voice mode
rem voice listen           # Single voice input & response
rem voice wake_word        # Waits for "Hey REM" trigger
rem voice always_on        # Always listening (experimental)

# Service health
rem health
```

### 2️⃣ HTTP Bridge API (for OpenClaw)

Start the HTTP RPC server:

```bash
# Start bridge (default: http://127.0.0.1:8765)
rem bridge

# Or with custom settings
rem bridge --host 0.0.0.0 --port 9000
```

Then call it from anywhere:

```bash
# Health check
curl http://127.0.0.1:8765/health

# Get service info
curl http://127.0.0.1:8765/info

# LLM generation
curl -X POST http://127.0.0.1:8765/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?"}'

# Chat
curl -X POST http://127.0.0.1:8765/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, how are you?"}'

# Web control
curl -X POST http://127.0.0.1:8765/web/control \
  -H "Content-Type: application/json" \
  -d '{"text": "search youtube for python"}'

# Generic RPC call
curl -X POST http://127.0.0.1:8765/call \
  -H "Content-Type: application/json" \
  -d '{"service": "llm_generate", "params": {"prompt": "test"}}'
```

### 3️⃣ OpenClaw Agent (Full AI Routing)

```bash
# Start OpenClaw in agent mode
cd openclaw
npm install  # First time only
node openclaw.mjs agent --mode rpc --json

# Then use OpenClaw's interface or voice to:
# - "Search YouTube for tutorials"
# - "What is machine learning?"
# - "Play music on YouTube"
# etc.
```

OpenClaw will automatically route requests to REM services.

### 4️⃣ Python API (for Custom Scripts)

```python
import asyncio
from server.rem_openclaw_adapter import get_adapter, RemService

async def main():
    adapter = get_adapter()
    
    # LLM
    result = await adapter.call_service(
        RemService.LLM_GENERATE,
        {"prompt": "What is Python?"},
        timeout=30
    )
    print(result["result"]["text"])
    
    # Web control
    result = await adapter.call_service(
        RemService.WEB_CONTROL,
        {"text": "search youtube for python"},
        timeout=10
    )
    print(result["result"]["detail"]["message"])

asyncio.run(main())
```

---

## 📁 Project Structure

```
Rem_project/
├── server/
│   ├── rem_openclaw_adapter.py      ← Core OpenClaw bridge
│   ├── openclaw_bridge.py           ← HTTP RPC server
│   ├── main_chat.py                 ← Voice assistant loop
│   └── process/
│       ├── web_control.py           ← YouTube/Google intent detection
│       ├── llm_funcs/llm_scr.py    ← LLM wrapper
│       ├── tts_func/sovits_ping.py ← TTS wrapper
│       └── asr_func/asr_push_to_talk.py ← ASR wrapper
│
├── openclaw/                        ← Full OpenClaw repo
│   └── skills/
│       └── rem-local/
│           └── SKILL.md   ← REM skill definition for OpenClaw
│
├── rem                              ← Python CLI entry point
├── rem.bat                          ← Windows batch wrapper
├── rem.ps1                          ← PowerShell wrapper
│
├── character_config.yaml            ← REM configuration
├── chat_history.json                ← Conversation memory
│
└── Documentation files...
```

---

## ⚙️ Configuration

### REM Settings (`character_config.yaml`)

```yaml
# Language model
model:
  name: "llama3.2"
  ollama_url: "http://127.0.0.1:11434"
  temperature: 0.7

# Text-to-speech (optional)
tts:
  enabled: true
  sovits_url: "http://127.0.0.1:9880"

# Speech recognition
asr:
  model: "base.en"
  language: "en"

# Web browsing
web_control:
  enabled: true
  browser: "default"  # or "chrome", "firefox", etc.
```

### Bridge Settings

Edit `server/openclaw_bridge.py` or pass command-line args:

```bash
rem bridge --host 127.0.0.1 --port 8765
```

---

## 🧪 Testing & Verification

### Test 1: Basic Health Check
```bash
rem health
# Expected: ✅ OLLAMA: Running, ❌ SOVITS: Down (or ✅ if available)
```

### Test 2: LLM Generation
```bash
rem llm "Hello, who are you?"
# Should respond with LLM-generated text
```

### Test 3: Web Control
```bash
rem web "search youtube for python programming"
# Browser should open with YouTube search results
```

### Test 4: HTTP API
```bash
# Start bridge in another terminal
rem bridge

# Test endpoint
curl http://127.0.0.1:8765/health | python -m json.tool
# Should return service status
```

### Test 5: Intent Detection
```bash
python -c "
from server.process.web_control import detect_intent
test_phrases = [
    'open youtube and search for python glasses',
    'google what is machine learning'
]
for phrase in test_phrases:
    intent, query = detect_intent(phrase)
    print(f'{phrase} -> {intent}: {query}')
"
```

---

## 🔧 Troubleshooting

### "rem command not found"
Use full path:
```bash
python rem llm "test"
```

### "Ollama not found"
Make sure Ollama is running:
```bash
ollama serve  # In another terminal
```

### "SoVITS not available"
TTS is optional. System works fine without it. To enable:
1. Start GPT-SoVITS service
2. Verify at http://127.0.0.1:9880
3. Update `character_config.yaml`

### "Bridge connection refused"
Make sure it's running:
```bash
rem bridge  # In another terminal
```

### "OpenClaw not found"
Already included in `./openclaw/` directory.

---

## 📊 Service Status

| Feature | Status | When? |
|---------|--------|-------|
| **LLM Generation** | ✅ Ready | Always |
| **Chat with History** | ✅ Ready | Always |
| **Text-to-Speech** | ⚠️ Optional | If SoVITS running |
| **Speech Recognition** | ✅ Ready | When recording |
| **Web Control** | ✅ Ready | Always |
| **Voice Interaction** | ✅ Ready | When mic available |
| **HTTP Bridge** | ✅ Ready | When `rem bridge` running |
| **OpenClaw Agent** | ✅ Ready | When `node openclaw.mjs` running |

---

## 🎯 Common Use Cases

### Use Case 1: Ask a Question
```bash
rem llm "What is the capital of France?"
```

### Use Case 2: Get YouTube Results
```bash
rem web "search youtube for how to learn python"
# Opens browser with results
```

### Use Case 3: Have a Conversation
```bash
rem llm-chat "Tell me about AI"
rem llm-chat "Can you explain that differently?"  # Remembers context
```

### Use Case 4: Voice Input
```bash
rem voice listen
# Speak into microphone
# System transcribes and responds
```

### Use Case 5: Full OpenClaw Routing
```bash
cd openclaw
node openclaw.mjs agent --mode rpc

# Then tell it anything via OpenClaw's interface
# It automatically routes requests to REM skills
```

---

## 📈 Performance & Limitations

### Performance
- **LLM Response:** 1-10 seconds (depends on system/model)
- **Web Control:** <1 second
- **Speech Recognition:** 2-5 seconds per sentence
- **Text-to-Speech:** 1-3 seconds per sentence (if available)

### Limitations
- Requires **Python 3.8+**
- Requires **Ollama** running locally (8GB+ RAM recommended)
- Optional **SoVITS** for TTS (GPU recommended)
- Windows/Mac/Linux compatible
- Best with >= 4 CPU cores

---

## 🚀 Advanced Topics

### Running as a Service
```bash
# Windows: Use Task Scheduler to run rem voice listen or rem bridge
# Linux/Mac: Use systemd or launchd
```

### Custom Skills
Add new services to `server/rem_openclaw_adapter.py`:

```python
class RemService(Enum):
    YOUR_CUSTOM_SKILL = "your_custom_skill"

# Then implement handler:
async def _your_custom_skill(self, params, timeout):
    # Your implementation
    pass
```

### Docker Deployment
Container ready (uses Python 3.8+ base image with dependencies).

### Environment Variables
```bash
export OLLAMA_URL=http://custom-host:11434
export SOVITS_URL=http://custom-host:9880
export CHAR_CONFIG=./custom_config.yaml
```

---

## 📞 Support

### Check Health Status
```bash
rem health
```

### Enable Debug Logging
```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Then run command
rem llm "test"
```

### View Documentation
- **Quick Start:** [QUICKSTART_OPENCLAW_REM.md](./QUICKSTART_OPENCLAW_REM.md)
- **Full Guide:** [OPENCLAW_REM_INTEGRATION_COMPLETE.md](./OPENCLAW_REM_INTEGRATION_COMPLETE.md)
- **OpenClaw Skill:** [openclaw/skills/rem-local/SKILL.md](./openclaw/skills/rem-local/SKILL.md)

---

## 📜 License & Attribution

- **REM:** This project
- **OpenClaw:** https://github.com/openclaw/openclaw (MIT License)
- **Ollama:** https://ollama.ai
- **Whisper:** OpenAI
- **GPT-SoVITS:** Open source
- **FastAPI:** https://fastapi.tiangolo.com

---

## ✨ Summary

You now have a **complete, production-ready AI assistant** that:

✅ Runs entirely locally (no cloud dependencies)  
✅ Understands voice and text commands  
✅ Integrates with OpenClaw for advanced routing  
✅ Provides an HTTP API for external tools  
✅ Offers Python API for custom scripts  
✅ Maintains conversation history  
✅ Controls web browser (YouTube/Google)  

**Start:** `rem health` → `rem voice listen` → Talk to your computer!

---

**Questions or issues?** Check the documentation files or review the code in `server/rem_openclaw_adapter.py`.
