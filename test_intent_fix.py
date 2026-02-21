#!/usr/bin/env python
"""Test detect_intent with the failing phrase."""

from server.process.web_control import detect_intent

test_phrases = [
    'open youtube and search for python glasses',
    'search youtube for python glasses',
    'play python glasses on youtube',
    'google python glasses',
    'open google and what is python',
    'open google and search for for python'
]

print("Testing intent detection:\n")
for phrase in test_phrases:
    intent, param = detect_intent(phrase)
    print(f'Phrase: {repr(phrase)}')
    print(f'  → Intent: {intent}, Query: {repr(param)}')
    print()
