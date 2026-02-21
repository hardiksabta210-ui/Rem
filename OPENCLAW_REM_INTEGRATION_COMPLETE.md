# 🚀 OpenClaw + REM Complete Integration Guide

**Date:** February 21, 2026  
**Status:** ✅ Ready for Production  

---

## 📋 What You Have

Your REM project now includes:

1. **REM Adapter** (`server/rem_openclaw_adapter.py`) — Maps REM services to OpenClaw
2. **Web Control Skill** (`server/process/web_control.py`) — Opens YouTube/Google from voice
3. **OpenClaw Bridge** (`server/openclaw_bridge.py`) — HTTP RPC server for OpenClaw to call REM
4. **OpenClaw Repo** (`./openclaw/`) — Full OpenClaw source code
5. **REM Skill Doc** (`openclaw/skills/rem-local/SKILL.md`) — Instructions for OpenClaw LLM

---

## 🏗️ Architecture

```
🎤 Voice Input
    ↓
📱 REM (Python) ← Always-on local assistant
    ↓
   Adapter Layer (ExposeREM services as OpenClaw skills)
    ↓
🤖 OpenClaw Agent (Node.js)
    ↓
🔀 Skills Router
    ├─ LLM (Ollama) — Text generation
    ├─ TTS (SoVITS) — Speech synthesis
    ├─ ASR (Whisper) — Speech recognition
    ├─ Web Control — Browser automation
    └─ ...other skills...
```

---

## ✅ Setup Instructions

### Step 1: Install Dependencies

```bash
# Navigate to project
cd "C:\Users\hardi\Chat bot\Rem_project"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install REM requirements (already done, but verify)
pip install -r server/requirements_api.txt

# Verify FastAPI/uvicorn
pip list | grep -E "fastapi|uvicorn"
```

### Step 2: Start Local Services

**In separate terminals:**

```bash
# Terminal 1: Start Ollama (LLM backend)
ollama serve

# Terminal 2: Start GPT-SoVITS (TTS backend, optional)
# Run from wherever SoVITS is installed
python run.py

# Terminal 3: Start REM Bridge Service
cd "C:\Users\hardi\Chat bot\Rem_project"
.\.venv\Scripts\Activate.ps1
python server/openclaw_bridge.py
```

This starts the REM bridge on `http://127.0.0.1:8765`.

### Step 3 (Optional): Start OpenClaw Agent

```bash
# Terminal 4: Start OpenClaw
cd openclaw
npm install  # First time only
node openclaw.mjs agent --mode rpc --json
```

**Or use the simpler REM CLI directly** (no OpenClaw required):

```bash
# Terminal 4: Just use REM
rem llm "What is Python?"
rem web "search youtube for python tutorials"
rem voice listen
```

---

## 🎯 How to Use

### Option A: Direct REM Commands (Simplest)

```bash
# Text generation
rem llm "Explain quantum computing"

# Chat with history
rem llm-chat "Hello"
rem llm-chat "What did we just talk about?"

# Text to speech
rem tts "Hello world"

# Speech recognition
rem asr "audio/sample.wav"

# Web searches
rem web "search youtube for cat videos"
rem web "google what is AI"

# Voice interaction
rem voice listen

# Check health
rem health
```

### Option B: HTTP API (for OpenClaw Integration)

**Start the bridge:**
```bash
python server/openclaw_bridge.py
```

**Then call it:**
```bash
# Health check
curl http://127.0.0.1:8765/health

# Get service info
curl http://127.0.0.1:8765/info

# Call LLM
curl -X POST http://127.0.0.1:8765/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?"}'

# Chat
curl -X POST http://127.0.0.1:8765/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Web control
curl -X POST http://127.0.0.1:8765/web/control \
  -H "Content-Type: application/json" \
  -d '{"text": "search youtube for python"}'

# GenericRPC call
curl -X POST http://127.0.0.1:8765/call \
  -H "Content-Type: application/json" \
  -d '{
    "service": "llm_generate",
    "params": {"prompt": "What is machine learning?"},
    "timeout": 30
  }'
```

### Option C: Python API (for Custom Scripts)

```python
import asyncio
from server.rem_openclaw_adapter import get_adapter, RemService

async def main():
    adapter = get_adapter()
    
    # LLM Generation
    result = await adapter.call_service(
        RemService.LLM_GENERATE,
        {"prompt": "What is Python?"},
        timeout=30
    )
    print(result["result"]["text"])
    
    # Web Control
    result = await adapter.call_service(
        RemService.WEB_CONTROL,
        {"text": "search youtube for python"},
        timeout=10
    )
    print(result["result"]["detail"]["message"])

asyncio.run(main())
```

### Option D: OpenClaw Agent (Full AI Integration)

```bash
# Start OpenClaw agent
cd openclaw
node openclaw.mjs agent --mode rpc --json

# Then say (via voice or OpenClaw interface):
# "Search YouTube for cat videos"
# "What is machine learning?"
# "Play music on YouTube and tell me what you're doing"
```

OpenClaw's agent will:
1. Understand the intent
2. Choose the appropriate skill (REM skill)
3. Call the REM bridge service
4. Execute the command
5. Return results to the user

---

## 🔌 Configuration

### REM Settings (`character_config.yaml`)

```yaml
# LLM
model:
  name: "llama3.2"
  ollama_url: "http://127.0.0.1:11434"
  temperature: 0.7
  
# TTS
tts:
  enabled: true
  sovits_url: "http://127.0.0.1:9880"
  
# ASR
asr:
  model: "base.en"
  language: "en"
  
# Web browsing
web_control:
  enabled: true
  browser: "default"
```

### Bridge Configuration

Edit `server/openclaw_bridge.py` for custom:
- Host/port: Default `127.0.0.1:8765`
- Timeout settings
- Logging levels

---

## 🧪 Testing

### Test 1: Health Check

```bash
rem health
```

Expected output:
```
✅ OLLAMA: Running
❌ SOVITS: Down  (optional)
```

### Test 2: Basic LLM

```bash
rem llm "Hello, who are you?"
```

### Test 3: Web Control

```bash
rem web "search youtube for python programming"
```

Browser should open with YouTube search results.

### Test 4: HTTP API

```bash
# In another terminal while REM bridge is running:
curl http://127.0.0.1:8765/health | python -m json.tool
```

### Test 5: OpenClaw Integration

If OpenClaw running:
```bash
curl -X POST http://127.0.0.1:8765/call \
  -H "Content-Type: application/json" \
  -d '{"service": "llm_generate", "params": {"prompt": "test"}}'
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `server/rem_openclaw_adapter.py` | Core REM ↔ OpenClaw bridge |
| `server/openclaw_bridge.py` | HTTP RPC server for OpenClaw |
| `server/main_chat.py` | Main voice loop with web control |
| `server/process/web_control.py` | Intent detection + browser opening |
| `rem` | Python CLI entry point |
| `rem.bat` / `rem.ps1` | Windows shortcuts |
| `openclaw/` | Full OpenClaw repository |
| `openclaw/skills/rem-local/SKILL.md` | REM skill definition for OpenClaw |

---

## 🚦 Common Issues & Fixes

### Issue: "Ollama not running"

```bash
# Make sure Ollama is started
ollama serve

# Verify it's accessible
curl http://127.0.0.1:11434/api/tags
```

### Issue: "SoVITS (TTS) not available"

TTS is optional. System will work fine without it.  
To enable: Start SoVITS and set `sovits_url` in `character_config.yaml`.

### Issue: "Bridge connection refused"

```bash
# Make sure bridge is running in a separate terminal
python server/openclaw_bridge.py

# Verify endpoint
curl http://127.0.0.1:8765/health
```

### Issue: "Command not found: rem"

Use the full Python call:
```bash
python rem llm "test"

# Or use the batch wrapper
rem.bat llm "test"
```

### Issue: "Browser not opening (web control)"

Ensure `webbrowser` module is available:
```bash
python -c "import webbrowser; webbrowser.open('https://www.youtube.com')"
```

---

## 📊 Capabilities Summary

| Feature | Status | Method |
|---------|--------|--------|
| **LLM Generation** | ✅ Ready | `rem llm`, HTTP API, Python API |
| **Chat with History** | ✅ Ready | `rem llm-chat`, HTTP API |
| **Text-to-Speech** | ⚠️ Optional (SoVITS) | `rem tts`, HTTP API |
| **Speech Recognition** | ✅ Ready | `rem asr`, HTTP API |
| **Web Control** | ✅ Ready | `rem web`, HTTP API |
| **Voice Interaction** | ✅ Ready | `rem voice listen`, voice modes |
| **OpenClaw Agent** | ✅ Ready | Full integration via HTTP API |
| **Health Monitoring** | ✅ Ready | `rem health`, HTTP API |

---

## 🎓 Next Steps

1. **Start small:** Use `rem llm` and `rem web` commands first
2. **Test HTTP API:** Verify bridge works with curl commands
3. **Run voice mode:** Try `rem voice listen` for interactive mode
4. **Optional OpenClaw:** Start OpenClaw agent if you want full AI routing
5. **Custom skills:** Add more REM skills to the adapter as needed

---

## 📞 Support & Debugging

### Enable Debug Logging

```bash
# Set Python logging
python server/openclaw_bridge.py --loglevel DEBUG

# Or in code:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check OpenClaw Skills

```bash
cd openclaw
node openclaw.mjs skill list
node openclaw.mjs skill read rem-local
```

### Verify Service Connectivity

```bash
# All services at once
python -c "
from server.rem_openclaw_adapter import get_adapter
import asyncio
adapter = get_adapter()
async def test():
    result = await adapter.call_service(
        'HEALTH_CHECK', {}, timeout=5
    )
    print(result)
asyncio.run(test())
"
```

---

## ✨ You're Ready!

Your REM project now has:
- ✅ Local AI assistant with voice, LLM, TTS, ASR
- ✅ Web automation (YouTube/Google searches)
- ✅ OpenClaw integration (HTTP API)
- ✅ Full documentation
- ✅ CLI and Python API access

**Start with:** `rem health` to verify everything is working!

---

**Questions?** Check the OpenClaw docs: https://github.com/openclaw/openclaw
