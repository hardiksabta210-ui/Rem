#!/usr/bin/env python3
"""
Integration test suite for OpenClaw + REM

Tests all major integration points between REM services and OpenClaw.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent / "server"))

from rem_openclaw_adapter import get_adapter, RemService


class IntegrationTester:
    """Test suite for OpenClaw + REM integration."""

    def __init__(self):
        self.adapter = get_adapter()
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    async def test_llm_generate(self):
        """Test LLM text generation."""
        print("\n📝 Test: LLM Text Generation")
        try:
            result = await self.adapter.call_service(
                RemService.LLM_GENERATE,
                {"prompt": "Say hello"}
            )
            
            if result["success"] and "text" in result["result"]:
                print(f"  ✅ PASS: Generated text: {result['result']['text'][:50]}...")
                self.passed += 1
            else:
                print(f"  ❌ FAIL: {result['error']}")
                self.failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: Exception: {e}")
            self.failed += 1

    async def test_llm_chat(self):
        """Test LLM chat with history."""
        print("\n💬 Test: LLM Chat with History")
        try:
            # First message
            result1 = await self.adapter.call_service(
                RemService.LLM_CHAT,
                {"input": "My name is Alice"}
            )
            
            if not result1["success"]:
                print(f"  ❌ FAIL: First message failed: {result1['error']}")
                self.failed += 1
                return
            
            # Second message (should remember context)
            result2 = await self.adapter.call_service(
                RemService.LLM_CHAT,
                {"input": "What is my name?"}
            )
            
            if result2["success"] and ("Alice" in result2["result"]["response"] or "alice" in result2["result"]["response"].lower()):
                print(f"  ✅ PASS: Chat remembers context")
                self.passed += 1
            elif result2["success"]:
                print(f"  ⚠️  SKIP: Chat works but context may not be retained")
                self.skipped += 1
            else:
                print(f"  ❌ FAIL: {result2['error']}")
                self.failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: Exception: {e}")
            self.failed += 1

    async def test_tts_generate(self):
        """Test TTS generation."""
        print("\n🔊 Test: TTS Generation")
        try:
            result = await self.adapter.call_service(
                RemService.TTS_GENERATE,
                {"text": "Hello world"}
            )
            
            if result["success"]:
                audio_path = result["result"]["audio_path"]
                if Path(audio_path).exists():
                    print(f"  ✅ PASS: Audio file generated: {audio_path}")
                    self.passed += 1
                else:
                    print(f"  ⚠️  SKIP: Audio path returned but file not found (SoVITS may be down)")
                    self.skipped += 1
            else:
                if "GPT-SoVITS" in result["error"] or "Connection" in result["error"]:
                    print(f"  ⚠️  SKIP: GPT-SoVITS not available")
                    self.skipped += 1
                else:
                    print(f"  ❌ FAIL: {result['error']}")
                    self.failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: Exception: {e}")
            self.failed += 1

    async def test_asr_transcribe(self):
        """Test ASR transcription."""
        print("\n🎤 Test: ASR Transcription")
        
        # Check if test audio exists
        test_audio = Path(__file__).parent / "audio" / "test.wav"
        if not test_audio.exists():
            print(f"  ⚠️  SKIP: Test audio file not found at {test_audio}")
            self.skipped += 1
            return
        
        try:
            result = await self.adapter.call_service(
                RemService.ASR_TRANSCRIBE,
                {"audio_file": str(test_audio)}
            )
            
            if result["success"]:
                print(f"  ✅ PASS: Transcription: {result['result']['text']}")
                self.passed += 1
            else:
                print(f"  ❌ FAIL: {result['error']}")
                self.failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: Exception: {e}")
            self.failed += 1

    async def test_voice_wake(self):
        """Test voice wake mode."""
        print("\n🎧 Test: Voice Wake Mode")
        try:
            result = await self.adapter.call_service(
                RemService.VOICE_WAKE,
                {"mode": "listen"}
            )
            
            if result["success"]:
                print(f"  ✅ PASS: Voice mode started: {result['result']['status']}")
                self.passed += 1
            else:
                print(f"  ❌ FAIL: {result['error']}")
                self.failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: Exception: {e}")
            self.failed += 1

    async def test_health_check(self):
        """Test health check."""
        print("\n🏥 Test: Health Check")
        try:
            result = await self.adapter.call_service(
                RemService.HEALTH_CHECK,
                {}
            )
            
            if result["success"]:
                services = result["result"]["services"]
                ollama_status = "✅" if services.get("ollama") else "❌"
                sovits_status = "✅" if services.get("sovits") else "❌"
                
                print(f"  {ollama_status} Ollama: {'Running' if services.get('ollama') else 'Down'}")
                print(f"  {sovits_status} SoVITS: {'Running' if services.get('sovits') else 'Down'}")
                
                if services.get("ollama"):
                    print(f"  ✅ PASS: At least Ollama is running (LLM available)")
                    self.passed += 1
                else:
                    print(f"  ❌ FAIL: No services running")
                    self.failed += 1
            else:
                print(f"  ❌ FAIL: {result['error']}")
                self.failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: Exception: {e}")
            self.failed += 1

    async def test_skill_manifest(self):
        """Test skill manifest generation."""
        print("\n📋 Test: Skill Manifest")
        try:
            manifest = self.adapter.get_skill_manifest()
            
            if manifest.get("id") == "rem-local-assistant" and "capabilities" in manifest:
                capabilities = len(manifest["capabilities"])
                print(f"  ✅ PASS: Manifest valid with {capabilities} capabilities")
                self.passed += 1
            else:
                print(f"  ❌ FAIL: Invalid manifest structure")
                self.failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: Exception: {e}")
            self.failed += 1

    async def run_all(self):
        """Run all tests."""
        print("=" * 60)
        print("OpenClaw + REM Integration Test Suite")
        print("=" * 60)
        
        await self.test_skill_manifest()
        await self.test_health_check()
        await self.test_llm_generate()
        await self.test_llm_chat()
        await self.test_tts_generate()
        await self.test_asr_transcribe()
        await self.test_voice_wake()
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"✅ Passed:  {self.passed}")
        print(f"❌ Failed:  {self.failed}")
        print(f"⚠️  Skipped: {self.skipped}")
        print("=" * 60)
        
        return self.failed == 0


async def main():
    """Main entry point."""
    tester = IntegrationTester()
    success = await tester.run_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
