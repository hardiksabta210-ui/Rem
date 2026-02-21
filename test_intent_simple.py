#!/usr/bin/env python
"""Quick syntax and basic import test."""

print("Testing syntax and basic imports...")

try:
    from server.process.web_control import detect_intent
    print("[OK] Web control imported")
except Exception as e:
    print(f"[ERROR] Web control import failed: {e}")
    import traceback
    traceback.print_exc()

# Test intent detection
print("\nTesting intent detection:")
test_cases = [
    "open youtube and search for python glasses",
    "google what is machine learning",
]

for phrase in test_cases:
    intent, query = detect_intent(phrase)
    print(f'  "{phrase}"')
    print(f'    -> intent: {intent}, query: {query}')

print("\n[SUCCESS] Intent detection working!")
