#!/usr/bin/env python
"""Validate detect_intent with test phrases."""
import re
from typing import Tuple

def detect_intent(text: str) -> Tuple[str, str]:
    """Test version of detect_intent."""
    text_lower = text.lower().strip()

    # === Step 1: Check for YOUTUBE intents (highest priority) ===
    
    # 1a) "open youtube and search for X" or "open youtube and search X"
    m = re.search(r"open\s+youtube\s+and\s+search(?:\s+for)?\s+(.+?)(?:$|\.|\!|\?)", text_lower)
    if m:
        query = m.group(1).strip()
        if query:
            return "youtube_search", query
    
    # 1b) "search youtube for X" or "search for X on youtube"
    m = re.search(r"search\s+(?:youtube\s+)?for\s+(.+?)(?:$|\.|\!|\?)", text_lower)
    if m and 'youtube' in text_lower:
        query = m.group(1).strip()
        if query:
            return "youtube_search", query
    
    # 1c) "play X on youtube" or "play X youtube"
    m = re.search(r"play\s+(.+?)(?:\s+on\s+)?youtube", text_lower)
    if m:
        query = m.group(1).strip()
        if query:
            return "youtube_search", query
    
    # 1d) Bare "open youtube" (no search term)
    if re.search(r"^open\s+youtube$", text_lower):
        return "open_url", "youtube.com"
    
    # === Step 2: Check for GOOGLE intents ===
    
    # 2a) "google X" or "google search X"
    m = re.search(r"google\s+(?:search\s+)?(.+?)(?:$|\.|\!|\?)", text_lower)
    if m:
        query = m.group(1).strip()
        if query and 'youtube' not in query:
            return "google_search", query
    
    # 2b) "search for X" (when not on youtube)
    m = re.search(r"search\s+(?:for\s+)?(.+?)(?:$|\.|\!|\?)", text_lower)
    if m and 'youtube' not in text_lower:
        query = m.group(1).strip()
        if query:
            return "google_search", query
    
    # 2c) "look up X"
    m = re.search(r"look\s+up\s+(.+?)(?:$|\.|\!|\?)", text_lower)
    if m:
        query = m.group(1).strip()
        if query:
            return "google_search", query
    
    # === Step 3: Fallback ===
    if 'youtube' in text_lower:
        q = re.sub(r"^(open|search|play|search\s+youtube|search\s+for|play\s+on)\s+", "", text_lower)
        q = re.sub(r"\s+(?:on\s+)?youtube$", "", q)
        q = q.strip().rstrip('.?!')
        if q:
            return "youtube_search", q
        return "open_url", "youtube.com"

    return None, ""


# Test cases
test_cases = [
    ("open youtube and search for python glasses", "youtube_search", "python glasses"),
    ("search youtube for music", "youtube_search", "music"),
    ("play funny videos on youtube", "youtube_search", "funny videos"),
    ("google python", "google_search", "python"),
    ("search for weather", "google_search", "weather"),
    ("look up machine learning", "google_search", "machine learning"),
    ("open youtube", "open_url", "youtube.com"),
    ("open google and what is python", "google_search", "what is python"),
    ("open google and search for for python", "google_search", "for python"),
]

print("Testing intent detection:\n")
passed = 0
failed = 0

for phrase, expected_intent, expected_query in test_cases:
    intent, query = detect_intent(phrase)
    status = "✓" if (intent == expected_intent and query == expected_query) else "✗"
    
    if intent == expected_intent and query == expected_query:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} '{phrase}'")
    print(f"    Expected: {expected_intent}, {repr(expected_query)}")
    print(f"    Got:      {intent}, {repr(query)}")
    print()

print(f"\nResults: {passed} passed, {failed} failed")
