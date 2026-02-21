# Quick Start: OpenClaw + REM Integration

## 🚀 30-Second Setup

```bash
# 1. Navigate to project
cd "C:\Users\hardi\Chat bot\Rem_project"

# 2. Activate environment
.\.venv\Scripts\Activate.ps1

# 3. Test the setup (all should work)
rem health
rem llm "What is AI?"
rem web "search youtube for python"
```

## 🎯 Next Level: Add OpenClaw Bridge

```bash
# In Terminal 1: Start local services
ollama serve

# In Terminal 2: Start the REM bridge (http api for openclaw)
python server/openclaw_bridge.py

# In Terminal 3: Test the bridge
curl http://127.0.0.1:8765/health
```

## 🤖 Full Integration: Run OpenClaw Agent

```bash
# In Terminal 4: Start OpenClaw agent
cd openclaw
node openclaw.mjs agent --mode rpc --json

# Then say or send text:
# "Search YouTube for cat videos"
# "What is machine learning?"
# Open OpenClaw's interface and use it
```

---

## 📋 What Each Command Does

| Command | Purpose | Example |
|---------|---------|---------|
| `rem llm` | Generate text with AI | `rem llm "Explain Python"` |
| `rem llm-chat` | Chat bot with memory | `rem llm-chat "Hello"` |
| `rem web` | Search YouTube/Google | `rem web "youtube python tutorials"` |
| `rem tts` | Convert text to speech | `rem tts "Hello world"` |
| `rem asr` | Transcribe audio | `rem asr "audio/sample.wav"` |
| `rem voice` | Real-time voice mode | `rem voice listen` |
| `rem bridge` | Start HTTP API for OpenClaw | `rem bridge --port 8765` |
| `rem health` | Check service status | `rem health` |

---

## 🏗️ Architecture

```
Your REM Project (Python)
  ├─ LLM: Ollama (local, fast)
  ├─ TTS: GPT-SoVITS (optional, local)
  ├─ ASR: Whisper (speech-to-text)
  └─ Web: Browser automation (YouTube/Google)

OpenClaw Bridge (HTTP RPC Layer)
  └─ Exposes REM services via REST API

OpenClaw Agent (Node.js, optional)
  └─ AI routing and skill management
```

---

## ✅ Verify Installation

```bash
# Test 1: CLI works
rem health

# Test 2: HTTP API available
python server/openclaw_bridge.py &
curl http://127.0.0.1:8765/health

# Test 3: LLM responds
rem llm "Hello"

# Test 4: Web control works
rem web "search youtube for cats"
```

All should succeed!

---

## 🎓 Common Next Steps

1. **Use voice mode:** `rem voice listen` → speak to your computer
2. **Run full OpenClaw:** See OPENCLAW_REM_INTEGRATION_COMPLETE.md
3. **Add custom skills:** Extend `server/rem_openclaw_adapter.py`
4. **Deploy:** Container or systemd service for always-on

---

**That's it!** You now have:
- ✅ Local AI assistant (REM)
- ✅ OpenClaw integration (HTTP API)
- ✅ Full voice + web control
- ✅ Optional OpenClaw agent for routing

**Questions?** Check documentation files in the project root.
