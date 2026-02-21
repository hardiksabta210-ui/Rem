#!/usr/bin/env python3
"""
Test REM + OpenClaw Services
Verifies all services are working correctly
"""

import requests
import time
import sys
from pathlib import Path

def test_rem_api():
    """Test REM API Server"""
    print("\n[*] Testing REM API Server...")
    try:
        # Health check
        response = requests.get('http://127.0.0.1:8000/health', timeout=5)
        if response.status_code == 200:
            print("[✓] REM API Server is responding")
            data = response.json()
            print(f"    Status: {data.get('status')}")
            return True
        else:
            print(f"[!] REM API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[!] Cannot connect to REM API (port 8000)")
        print("    Make sure REM API Server is running")
        return False
    except Exception as e:
        print(f"[!] Error testing REM API: {e}")
        return False

def test_openclaw_bridge():
    """Test OpenClaw Bridge"""
    print("\n[*] Testing OpenClaw Bridge...")
    try:
        # Health check
        response = requests.get('http://127.0.0.1:8765/health', timeout=5)
        if response.status_code == 200:
            print("[✓] OpenClaw Bridge is responding")
            data = response.json()
            print(f"    Status: {data.get('status')}")
            return True
        else:
            print(f"[!] Bridge returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[!] Cannot connect to OpenClaw Bridge (port 8765)")
        print("    Make sure OpenClaw Bridge is running")
        return False
    except Exception as e:
        print(f"[!] Error testing Bridge: {e}")
        return False

def test_llm_endpoint():
    """Test LLM endpoint"""
    print("\n[*] Testing LLM endpoint...")
    try:
        payload = {
            "prompt": "Hello",
            "temperature": 0.7
        }
        response = requests.post(
            'http://127.0.0.1:8000/llm/generate',
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("[✓] LLM endpoint working")
                print(f"    Response: {result.get('result', 'N/A')[:50]}...")
                return True
            else:
                error = result.get('error', 'Unknown error')
                print(f"[!] LLM error: {error}")
                if "Ollama" in error:
                    print("    Make sure Ollama is running: ollama serve")
                return False
        else:
            print(f"[!] LLM returned status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("[!] LLM request timed out")
        print("    Make sure Ollama is running: ollama serve")
        return False
    except requests.exceptions.ConnectionError:
        print("[!] Cannot connect to REM API")
        return False
    except Exception as e:
        print(f"[!] Error testing LLM: {e}")
        return False

def test_bridge_call():
    """Test bridge service call"""
    print("\n[*] Testing Bridge service call...")
    try:
        payload = {
            "service": "llm_generate",
            "params": {"prompt": "Hi"}
        }
        response = requests.post(
            'http://127.0.0.1:8765/call',
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("[✓] Bridge service call working")
                return True
            else:
                error = result.get('error', 'Unknown error')
                print(f"[!] Bridge error: {error}")
                return False
        else:
            print(f"[!] Bridge returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[!] Error testing bridge call: {e}")
        return False

def main():
    print("="*60)
    print("  REM + OPENCLAW SERVICES TEST")
    print("="*60)
    
    print("\n[*] Waiting for services to be ready (assume they're already running)...")
    time.sleep(2)
    
    results = {
        "REM API": test_rem_api(),
        "OpenClaw Bridge": test_openclaw_bridge(),
        "LLM Endpoint": test_llm_endpoint(),
        "Bridge Call": test_bridge_call()
    }
    
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    for name, passed in results.items():
        status = "[✓]" if passed else "[!]"
        print(f"{status} {name}")
    
    all_pass = all(results.values())
    
    print("\n" + "="*60)
    if all_pass:
        print("  ✓ ALL TESTS PASSED!")
        print("  Services are working correctly")
    else:
        print("  ! SOME TESTS FAILED")
        print("  Check the errors above and restart services")
    print("="*60 + "\n")
    
    return 0 if all_pass else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
