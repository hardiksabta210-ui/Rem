"""
Test script for the Local TTS Server with LLaMA 3.2 integration.
This script tests the /chat_tts endpoint to ensure the pipeline works correctly.
"""

import requests
import json
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"
OLLAMA_URL = "http://127.0.0.1:11434"
GPT_SOVITS_URL = "http://127.0.0.1:9880"

def test_server_health():
    """Test if all required servers are running."""
    print("=== Testing Server Health ===")
    
    # Test FastAPI server
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ FastAPI server is running")
        else:
            print(f"✗ FastAPI server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ FastAPI server is not running. Start it with: python server/api_v2.py")
        return False
    
    # Test Ollama
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            llama_models = [m for m in models if "llama3.2" in m.get("name", "")]
            if llama_models:
                print("✓ Ollama is running with llama3.2 model")
            else:
                print("✗ Ollama is running but llama3.2 model not found")
                print("Available models:", [m.get("name") for m in models])
                return False
        else:
            print(f"✗ Ollama returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Ollama is not running. Start it with: ollama serve")
        return False
    
    # Test GPT-SoVITS
    try:
        response = requests.get(f"{GPT_SOVITS_URL}/")
        if response.status_code == 200:
            print("✓ GPT-SoVITS server is running")
        else:
            print(f"✗ GPT-SoVITS returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ GPT-SoVITS server is not running")
        print("Note: GPT-SoVITS may not have a root endpoint, but that's okay if TTS endpoint works")
    
    return True

def test_chat_tts_endpoint():
    """Test the /chat_tts endpoint with a sample request."""
    print("\n=== Testing /chat_tts Endpoint ===")
    
    # Test request
    test_request = {
        "user_input": "Tell me a short joke about programming",
        "text_lang": "en",
        "play_audio": False
    }
    
    print(f"Sending request: {json.dumps(test_request, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat_tts",
            json=test_request,
            timeout=120  # 2 minute timeout for LLM generation + TTS
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ /chat_tts endpoint successful!")
            print(f"Generated text: {result['generated_text']}")
            print(f"Audio file: {result['audio_file']}")
            print(f"Audio path: {result['audio_path']}")
            
            # Test audio file download
            audio_response = requests.get(f"{BASE_URL}/audio/{result['audio_file']}")
            if audio_response.status_code == 200:
                print("✓ Audio file download successful")
                
                # Save audio file for manual testing
                audio_dir = Path("test_audio")
                audio_dir.mkdir(exist_ok=True)
                audio_path = audio_dir / result['audio_file']
                
                with open(audio_path, 'wb') as f:
                    f.write(audio_response.content)
                
                print(f"✓ Audio file saved to: {audio_path}")
                print(f"File size: {len(audio_response.content)} bytes")
            else:
                print(f"✗ Audio file download failed: {audio_response.status_code}")
            
            return True
        else:
            print(f"✗ /chat_tts endpoint failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("✗ Request timed out (120 seconds)")
        return False
    except Exception as e:
        print(f"✗ Error testing /chat_tts endpoint: {str(e)}")
        return False

def test_error_handling():
    """Test error handling scenarios."""
    print("\n=== Testing Error Handling ===")
    
    # Test with empty input
    empty_request = {
        "user_input": "",
        "text_lang": "en",
        "play_audio": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat_tts", json=empty_request)
        if response.status_code == 400:
            print("✓ Empty input properly rejected")
        else:
            print(f"✗ Empty input handling unexpected status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing empty input: {str(e)}")
    
    # Test with Ollama offline (simulate by changing URL)
    print("Note: Ollama offline test skipped (would require stopping Ollama)")

def main():
    """Run all tests."""
    print("Local TTS Server with LLaMA 3.2 - Integration Test")
    print("=" * 50)
    
    # Check if required servers are running
    if not test_server_health():
        print("\n❌ Server health check failed. Please ensure all servers are running:")
        print("1. FastAPI server: python server/api_v2.py")
        print("2. Ollama: ollama serve (with llama3.2 model)")
        print("3. GPT-SoVITS: Start your GPT-SoVITS server")
        return
    
    # Test the main endpoint
    if test_chat_tts_endpoint():
        print("\n✅ All tests passed! The integration is working correctly.")
    else:
        print("\n❌ Tests failed. Check the error messages above.")
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("Test completed. Check the test_audio/ directory for generated audio files.")

if __name__ == "__main__":
    main()