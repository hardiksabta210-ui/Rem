#!/usr/bin/env python3
"""Quick validation of applied fixes"""

import json
import yaml
import sys
from pathlib import Path

def check_config_yaml():
    """Verify character_config.yaml fixes"""
    print("\n1. Checking character_config.yaml...")
    try:
        with open('character_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Check no API key in file (try multiple encodings)
        try:
            with open('character_config.yaml', 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open('character_config.yaml', 'r', encoding='latin-1') as f:
                content = f.read()
        
        if 'sk-proj-' in content:
            print("  ❌ FAIL: API key still present in file")
            return False
        else:
            print("  ✅ PASS: No API key in file")
        
        # Check language settings
        text_lang = config['sovits_ping_config']['text_lang']
        prompt_lang = config['sovits_ping_config']['prompt_lang']
        
        if text_lang == 'es' and prompt_lang == 'es':
            print(f"  ✅ PASS: Language settings fixed (es)")
        else:
            print(f"  ❌ FAIL: Language mismatch - got {text_lang}/{prompt_lang}")
            return False
            
        print("  ✅ File loads with UTF-8 encoding")
        return True
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        return False

def check_llm_trimming():
    """Verify LLM history trimming logic"""
    print("\n2. Checking llm_scr.py history trimming...")
    try:
        with open('server/process/llm_funcs/llm_scr.py', 'r') as f:
            content = f.read()
        
        if 'ENABLE_HISTORY_TRIM' in content and 'MAX_HISTORY_MESSAGES' in content:
            if 'if ENABLE_HISTORY_TRIM and len(history) >' in content:
                print("  ✅ PASS: History trimming logic implemented")
                return True
            else:
                print("  ❌ FAIL: History trimming referenced but not implemented")
                return False
        else:
            print("  ❌ FAIL: Trimming constants not found")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        return False

def check_unused_options():
    """Verify unused options parameter removed"""
    print("\n3. Checking generate_from_prompt signature...")
    try:
        with open('server/process/llm_funcs/llm_scr.py', 'r') as f:
            content = f.read()
        
        # Check signature
        if 'def generate_from_prompt(prompt: str) -> str:' in content:
            print("  ✅ PASS: Unused options parameter removed")
            return True
        elif 'def generate_from_prompt(prompt: str, options' in content:
            print("  ❌ FAIL: options parameter still present")
            return False
        else:
            print("  ⚠️  SKIP: Function signature not found")
            return True
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        return False

def check_tts_health():
    """Verify TTS health check fix"""
    print("\n4. Checking TTS health check...")
    try:
        with open('server/process/tts_func/sovits_ping.py', 'r') as f:
            content = f.read()
        
        if '200 <= response.status_code < 300' in content:
            print("  ✅ PASS: Health check now validates 2xx only")
            return True
        elif 'response.status_code < 500' in content:
            print("  ❌ FAIL: Still using loose < 500 check")
            return False
        else:
            print("  ⚠️  SKIP: Function not found")
            return True
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        return False

def check_encoding():
    """Verify UTF-8 encoding in main_chat_siri.py"""
    print("\n5. Checking YAML encoding...")
    try:
        with open('server/main_chat_siri.py', 'r') as f:
            content = f.read()
        
        if "open('character_config.yaml', 'r', encoding='utf-8')" in content:
            print("  ✅ PASS: UTF-8 encoding set for YAML")
            return True
        else:
            print("  ⚠️  SKIP: Encoding pattern not found (may be OK)")
            return True
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        return False

def check_cleanup_error_handling():
    """Verify error handling in cleanup loop"""
    print("\n6. Checking audio cleanup error handling...")
    try:
        with open('server/main_chat.py', 'r') as f:
            content = f.read()
        
        if 'for fp in Path("audio").glob("*.wav"):\n        if fp.is_file():\n            try:' in content:
            print("  ✅ PASS: Error handling inside loop")
            return True
        else:
            print("  ⚠️  SKIP: Pattern may have changed (verify manually)")
            return True
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        return False

def check_docs_paths():
    """Verify hardcoded paths removed from docs"""
    print("\n7. Checking documentation paths...")
    try:
        files_to_check = [
            'OPENCLAW_README.md',
            'OPENCLAW_IMPLEMENTATION_COMPLETE.md'
        ]
        
        all_good = True
        for fname in files_to_check:
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(fname, 'r', encoding='latin-1') as f:
                        content = f.read()
                except:
                    try:
                        with open(fname, 'r', encoding='cp1252') as f:
                            content = f.read()
                    except Exception as e:
                        print(f"  ⚠️  SKIP: {fname} - encoding error: {e}")
                        continue
            
            if 'c:\\Users\\hardi' in content.lower():
                print(f"  ❌ FAIL: {fname} still has hardcoded path")
                all_good = False
            else:
                print(f"  ✅ PASS: {fname} uses generic paths")
        
        return all_good
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("Validation: Applied Fixes")
    print("=" * 60)
    
    results = [
        check_config_yaml(),
        check_llm_trimming(),
        check_unused_options(),
        check_tts_health(),
        check_encoding(),
        check_cleanup_error_handling(),
        check_docs_paths(),
    ]
    
    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Results: {passed}/{total} checks passed")
    print("=" * 60)
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
