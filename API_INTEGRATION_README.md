# Local TTS Server with LLaMA 3.2 Integration

This integration adds Ollama LLaMA 3.2 text generation to your existing GPT-SoVITS TTS pipeline, creating a fully local AI voice assistant.

## Architecture Overview

```
User Input → Ollama LLaMA 3.2 → Generated Text → GPT-SoVITS → WAV Audio
     ↓              ↓                ↓              ↓           ↓
  HTTP Request → Local LLM → Plain Text Response → TTS Engine → Audio File
```

## Prerequisites

### Required Services
1. **Ollama** running locally at `http://127.0.0.1:11434`
   - Install: `ollama pull llama3.2`
   - Start: `ollama serve`

2. **GPT-SoVITS** server running at `http://127.0.0.1:9880`
   - Start your existing GPT-SoVITS server

3. **Python 3.10-3.11** with required packages

## Installation

1. Install new dependencies:
```bash
pip install -r server/requirements_api.txt
```

2. Ensure your `character_config.yaml` is properly configured with:
   - `sovits_ping_config` settings for GPT-SoVITS
   - Reference audio file path
   - Language settings

## Usage

### Start the Server
```bash
cd server
python api_v2.py
```

The server will start at `http://127.0.0.1:8000`

### API Endpoints

#### 1. Generate Speech from Text (`POST /chat_tts`)

**Request Format:**
```json
{
  "user_input": "Your message here",
  "text_lang": "en",  // Optional: en/ja/zh
  "play_audio": false  // Optional: true to play audio locally
}
```

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/chat_tts" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Tell me a short joke about programming",
    "text_lang": "en",
    "play_audio": false
  }'
```

**Response:**
```json
{
  "audio_file": "output_abc123.wav",
  "generated_text": "Why do programmers prefer dark mode? Because light attracts bugs!",
  "audio_path": "C:\\Users\\...\\audio\\output_abc123.wav"
}
```

#### 2. Download Audio File (`GET /audio/{filename}`)

```bash
curl -O "http://127.0.0.1:8000/audio/output_abc123.wav"
```

#### 3. Server Info (`GET /`)

Returns server status and requirements.

### Testing

Run the test script to verify everything works:

```bash
python test_api.py
```

This will:
- Check if all required servers are running
- Test the `/chat_tts` endpoint
- Verify audio file generation and download
- Test error handling

## Data Flow

1. **User Input**: Client sends text prompt to `/chat_tts`
2. **LLM Generation**: 
   - Server calls Ollama API at `http://127.0.0.1:11434/api/generate`
   - Uses `llama3.2` model with configurable parameters
   - Returns plain text response
3. **Text Validation**: Ensures LLM output is not empty
4. **TTS Synthesis**: 
   - Calls existing `sovits_gen()` function
   - Uses GPT-SoVITS at `http://127.0.0.1:9880/tts`
   - Saves audio to `audio/` directory
5. **Response**: Returns audio file info and generated text

## Error Handling

The integration includes comprehensive error handling:

- **Ollama Offline**: Clear error message if Ollama is not running
- **Empty LLM Output**: Rejects empty responses safely
- **TTS Failures**: Graceful handling of GPT-SoVITS errors
- **File Management**: Automatic cleanup and unique file naming
- **Timeouts**: 60-second timeout for LLM, 120-second for full pipeline

## Configuration

### Ollama Settings
Edit `server/api_v2.py` to modify:
- `OLLAMA_URL`: Change if Ollama runs on different port
- `OLLAMA_MODEL`: Use different model if available
- LLM parameters in `llm_generate_text()` function

### GPT-SoVITS Settings
Configure in `character_config.yaml`:
```yaml
sovits_ping_config:
  text_lang: en
  prompt_lang: en
  ref_audio_path: path/to/your/reference.wav
  prompt_text: "Your reference text here"
```

## Performance Notes

- **LLM Generation**: Typically 10-30 seconds depending on hardware
- **TTS Synthesis**: 5-15 seconds depending on text length
- **Total Pipeline**: 15-45 seconds end-to-end
- **Memory Usage**: LLaMA 3.2 ~4-8GB VRAM/CPU, GPT-SoVITS ~2-4GB

## Troubleshooting

### Common Issues

1. **"Cannot connect to Ollama server"**
   - Ensure Ollama is running: `ollama serve`
   - Check URL in `api_v2.py` matches your setup

2. **"Bad Request (400) from TTS server"**
   - Check `character_config.yaml` paths are correct
   - Verify reference audio file exists
   - Ensure GPT-SoVITS server is running

3. **"LLaMA 3.2 returned empty response"**
   - Check Ollama model is loaded: `ollama list`
   - Verify model name in config matches available models

4. **Audio playback issues**
   - Install sounddevice: `pip install sounddevice`
   - Check audio drivers and permissions

### Debug Mode

Add debug logging by modifying the logging level in `api_v2.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # Change from INFO to DEBUG
```

## Integration with Existing Code

The integration is designed to work alongside your existing code:

- **No changes to GPT-SoVITS**: Uses existing `sovits_gen()` function
- **No changes to LLM**: Keeps existing `llm_response()` for other uses
- **New API endpoint**: `/chat_tts` is separate from existing endpoints
- **Backward compatibility**: Existing code continues to work unchanged

## Security Notes

- All communication is local (127.0.0.1)
- No cloud APIs or external dependencies
- Audio files are stored locally in `audio/` directory
- Consider file cleanup policies for production use

## Next Steps

1. Start all required servers
2. Run `python test_api.py` to verify setup
3. Use the `/chat_tts` endpoint in your applications
4. Customize the LLM prompt or TTS settings as needed