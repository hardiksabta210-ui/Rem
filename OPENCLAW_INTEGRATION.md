# OpenClaw + REM Integration Guide

## Overview

The REM project is now integrated with **OpenClaw**, a multi-channel AI gateway. This document explains how to use the unified `rem` command to access both REM services and OpenClaw features.

## Quick Start

### Prerequisites

- Python 3.8+
- Ollama running on `http://127.0.0.1:11434` (for LLM)
- GPT-SoVITS running on `http://127.0.0.1:9880` (for TTS, optional)
- OpenClaw cloned in `/openclaw` directory
- Node.js >= 22 (for OpenClaw)

### Installation

1. **No additional setup needed** — OpenClaw is already cloned and REM commands are available:

```bash
# Windows PowerShell
.\rem help

# Windows Command Prompt
python rem help

# Or use the batch wrapper
rem.bat llm "hello"
```

## Commands

### LLM / Language Model

#### Generate text from a prompt
```bash
rem llm "Explain what is machine learning"
```

#### Chat with history
```bash
rem llm-chat "Hello, how are you?"
rem llm-chat "Tell me about Python"
rem llm-chat "What did we just talk about?"  # References conversation history
```

### Text-to-Speech (TTS)

#### Convert text to speech
```bash
rem tts "Hello world"
```

Generates audio file and displays path.

### Automatic Speech Recognition (ASR)

#### Transcribe audio file
```bash
rem asr "audio/sample.wav"
```

### Voice Modes

#### Start always-listening mode
```bash
rem voice listen
rem voice wake_word
rem voice always_on
```

### Health Check

#### Check service status
```bash
rem health
```

Output example:
```
🏥 Checking service health...

✅ Overall: Healthy

✅ OLLAMA: Running
✅ SOVITS: Running
```

### OpenClaw Commands

#### Access OpenClaw CLI directly
```bash
rem openclaw --help
rem openclaw agent --mode rpc --json
rem openclaw skill list
```

### Skill Manifest

#### Display available REM capabilities
```bash
rem manifest
```

Returns JSON skill manifest showing all capabilities and parameters for OpenClaw integration.

## Architecture

### Layer 1: REM Services
- **LLM** (`server/process/llm_funcs/llm_scr.py`) — Ollama wrapper
- **TTS** (`server/process/tts_func/sovits_ping.py`) — GPT-SoVITS wrapper
- **ASR** (`server/process/asr_func/`) — Whisper-based transcription
- **Voice** (`server/main_chat_siri.py`) — Always-listening assistant

### Layer 2: REM CLI
- **`rem`** — Python CLI entry point (cross-platform)
- **`rem.bat`** — Windows batch wrapper
- **`rem.ps1`** — Windows PowerShell wrapper

### Layer 3: OpenClaw Adapter
- **`server/rem_openclaw_adapter.py`** — Bridge between REM services and OpenClaw
  - Exposes REM services as async callables
  - Provides OpenClaw skill manifest
  - Handles service health checks
  - Manages error handling and timeouts

### Layer 4: OpenClaw
- **`openlaw/`** — Full OpenClaw repository (Node.js)
  - Gateway (control plane) on port 18789
  - CLI interface
  - Web UI and WebChat
  - Multi-channel support

## Integration Details

### Service Calls from OpenClaw

OpenClaw can call REM services via the adapter:

```typescript
// Example TypeScript (in OpenClaw)
const adapter = getRemAdapter();
const result = await adapter.call_service(
  RemService.LLM_CHAT,
  { input: "Tell me a joke" }
);
console.log(result.result.response);
```

### Available Services

Services exposed via `rem_openclaw_adapter.py`:

| Service | Endpoint | Parameters |
|---------|----------|------------|
| `llm.generate` | `LLM_GENERATE` | `prompt: str` |
| `llm.chat` | `LLM_CHAT` | `input: str` |
| `tts.generate` | `TTS_GENERATE` | `text: str, character?: str, emotion?: str` |
| `asr.transcribe` | `ASR_TRANSCRIBE` | `audio_file: str` |
| `voice.wake` | `VOICE_WAKE` | `mode: "listen"\|"wake_word"\|"always_on"` |
| `health.check` | `HEALTH_CHECK` | (no params) |

### Resource Timeouts

- LLM generation: 120 seconds
- TTS: 120 seconds
- ASR: 120 seconds (configurable)

## Examples

### Example 1: LLM Processing Pipeline

```bash
# Single query
rem llm "Write a poem about Python"

# Chat with context
rem llm-chat "What's Python?"
rem llm-chat "Tell me about its libraries"
rem llm-chat "Recommend a library for web development"
```

### Example 2: Voice Assistant Flow

```bash
# Check services are ready
rem health

# Start listening
rem voice listen

# Later, generate response
rem llm-chat "What did you say I should listen for?"

# Convert to speech
rem tts "I am listening carefully"
```

### Example 3: OpenClaw Integration

```bash
# Show all available skills
rem manifest

# Run OpenClaw gateway
rem openclaw start

# In another terminal, check skill availability
rem openclaw skill info rem-local-assistant
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'rem_openclaw_adapter'`

**Solution:** Ensure you're running from the project root:
```bash
cd c:\Users\hardi\Chat bot\Rem_project
python rem --help
```

### Services showing as "Down" in health check

**Ollama down:**
```bash
ollama serve
```

**GPT-SoVITS down:**
Ensure GPT-SoVITS server is running on port 9880. If not required, TTS commands will fail but other services work.

### Timeout errors

Increase service timeouts in `server/rem_openclaw_adapter.py`:
```python
OLLAMA_TIMEOUT_SEC = 300  # Increase from 120
```

### OpenClaw commands not found

Ensure Node.js >= 22 is installed:
```bash
node --version
```

## File Structure

```
c:\Users\hardi\Chat bot\Rem_project\
├── rem                         ← Main CLI (Python)
├── rem.bat                      ← Windows batch wrapper
├── rem.ps1                      ← Windows PowerShell wrapper
├── server/
│   ├── rem_openclaw_adapter.py  ← OpenClaw ↔ REM bridge
│   ├── process/
│   │   ├── llm_funcs/
│   │   │   └── llm_scr.py       (LLM service)
│   │   ├── tts_func/
│   │   │   └── sovits_ping.py   (TTS service)
│   │   └── asr_func/
│   │       └── asr_push_to_talk.py (ASR service)
│   ├── main_chat_siri.py        (Voice mode)
│   └── api_v2.py                (FastAPI endpoints)
├── openclaw/                    ← OpenClaw repo (Node.js)
│   ├── openclaw.mjs
│   ├── package.json
│   └── [other OpenClaw files]
└── character_config.yaml        ← Configuration

```

## Performance Tips

1. **Run Ollama with GPU** — Edit `character_config.yaml` for better LLM performance
2. **Cache TTS outputs** — Reuse generated speech files instead of regenerating
3. **Run OpenClaw in Docker** — Isolate Node.js from Python services
4. **Monitor memory** — Use `rem health` to catch service failures early

## Advanced Usage

### Running as a daemon

Create a batch script to run REM services in the background:

```batch
@echo off
start "REM Voice" cmd /k python rem voice listen
start "REM API" cmd /k python server/api_v2.py
start "OpenClaw" cmd /k node openclaw/openclaw.mjs start
```

### Integration with external systems

The `rem_openclaw_adapter.py` can be extended to integrate with:
- Web APIs (REST/GraphQL)
- Message queues (Kafka, RabbitMQ)
- IoT systems
- Third-party LLM APIs

### Extending with custom skills

Add new services in `rem_openclaw_adapter.py`:

```python
async def _custom_skill(self, params, timeout):
    # Your logic here
    return {
        "success": True,
        "result": {"output": "..."},
        "error": None
    }
```

## Next Steps

1. **Deploy OpenClaw** — Follow [OpenClaw deployment guide](../openclaw/docs/)
2. **Add channel integrations** — Configure Slack, Discord, WhatsApp, etc. in OpenClaw
3. **Fine-tune models** — Optimize Ollama and GPT-SoVITS for your use case
4. **Monitor and debug** — Enable detailed logging in adapter

---

For more information:
- **REM Project**: See [README.md](../README.md)
- **OpenClaw**: See [openclaw/README.md](../openclaw/README.md)
- **API Docs**: See [API_INTEGRATION_README.md](../API_INTEGRATION_README.md)
