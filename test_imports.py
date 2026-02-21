#!/usr/bin/env python
"""Quick test of the main_chat.py imports and adapter integration."""

import sys
from pathlib import Path

# Set up paths
server_dir = Path(__file__).parent / "server"
if str(server_dir) not in sys.path:
    sys.path.insert(0, str(server_dir))

print("Testing imports and adapter...")

try:
    from server.rem_openclaw_adapter import get_adapter, RemService
    print("[OK] Adapter imported")
except ImportError as e:
    print(f"[ERROR] Adapter import failed: {e}")
    sys.exit(1)

try:
    from server.process.web_control import detect_intent
    print("[OK] Web control imported")
except ImportError as e:
    print(f"[ERROR] Web control import failed: {e}")
    sys.exit(1)

# Test intent detection
print("\nTesting intent detection:")
test_cases = [
    "open youtube and search for python glasses",
    "google what is machine learning",
]

for phrase in test_cases:
    intent, query = detect_intent(phrase)
    print(f'  "{phrase}" -> {intent}: {query}')

# Test adapter initialization (no async call, just creation)
print("\nTesting adapter creation:")
try:
    adapter = get_adapter()
    print(f"[OK] Adapter instance created: {adapter}")
except Exception as e:
    print(f"[ERROR] Adapter creation failed: {e}")
    sys.exit(1)

print("\n[SUCCESS] All imports and basic tests passed!")
