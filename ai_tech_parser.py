import json
import os
from groq import Groq
from config import GROQ_API_KEY, AI_MODEL

_client = None

def get_ai_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def analyze_tech_update(title: str, content_snippet: str, source_url: str, update_type: str = "release") -> dict:
    """
    Uses Groq AI to analyze a new software release or tech article specifically
    for the 'Coding with Sudhir' YouTube channel.
    Generates a viral YouTube title, duration target, and a 3-step screen recording blueprint.
    """
    client = get_ai_client()
    
    prompt = f"""
You are an expert YouTube Tech Producer and Content Strategist for the channel 'Coding with Sudhir'.
The channel focuses on:
1. Fast, straight-to-the-point software/tool installation and setup on Windows 11 (Amit Thinks style).
2. Trending AI tools, free local AI setups (Ollama, DeepSeek, Cursor AI).
3. Practical developer error fixes ('command not recognized', PATH setup, ports).
4. Critical Security Bugs & Zero-Day Exploit Fixes (e.g., PHP Windows RCE bug, Node.js vulnerability, how developers can patch/fix immediately).

Analyze this tech update:
Title: {title}
Type: {update_type}
Source URL: {source_url}
Content Snippet: {content_snippet[:2000]}

Determine if this is worth creating a short YouTube tutorial or walkthrough for developers/students.
Respond in strict JSON format:
{{
  "is_worthy_for_video": true,
  "tool_name": "Name of the software, AI tool, or Bug/CVE (e.g., Python 3.14, Ollama v0.4, PHP CGI Bug CVE-2024-4577)",
  "category": "Software Version Release" or "Trending AI Tool" or "Critical Bug / Security Patch" or "Developer Utility",
  "why_viral": "1 punchy sentence explaining why coders/students are searching for this right now (panic, curiosity, or need to fix)",
  "youtube_title": "High-CTR, professional English YouTube title (e.g., How to Install Python 3.14 on Windows 11 | Full Setup, OR Critical PHP Bug on Windows: How to Fix Now!)",
  "target_duration": "2.5 Minutes" or "7-10 Minutes (if complex DB/server)",
  "screen_recording_blueprint": [
    "Step 1: Exactly what to open/download/show on screen in first 30 seconds (or show the vulnerability/bug)",
    "Step 2: What to configure, tick, or patch (e.g. Add to PATH, update version, edit config file)",
    "Step 3: Verification command in CMD/Terminal and testing"
  ],
  "youtube_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "hindi_tip_for_sudhir": "1 short friendly Hindi sentence guiding Sudhir on what to be careful about during recording"
}}

If the update is purely internal/trivial documentation or not useful for a video, set "is_worthy_for_video": false.
"""

    try:
        resp = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        print(f"AI Tech Analysis Error: {e}")
        return {
            "is_worthy_for_video": True,
            "tool_name": title,
            "category": "Software Release",
            "why_viral": "New update released for developers.",
            "youtube_title": f"How to Install {title} on Windows 11",
            "target_duration": "3 Minutes",
            "screen_recording_blueprint": [
                "Open official website and download installer",
                "Run setup and check Add to PATH",
                "Verify version in Command Prompt"
            ],
            "youtube_tags": ["install", "setup", "windows 11", "coding"],
            "hindi_tip_for_sudhir": "Bas 2-3 minute me download se lekar CMD verify tak dikha do."
        }
