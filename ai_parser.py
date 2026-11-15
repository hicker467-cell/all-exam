import json
from groq import Groq
from config import GROQ_API_KEY, AI_MODEL

_client = None

def get_ai_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def analyze_notice(raw_title: str, text_snippet: str, source_name: str) -> dict:
    """
    Uses Groq AI to extract structured dates, verify authenticity, filter old years,
    and generate student-friendly Hindi summary and YouTube metadata.
    """
    client = get_ai_client()
    
    prompt = f"""
You are an expert Indian exam notice analyzer for Sagar Coaching Centre.
Analyze this notice from source '{source_name}':
Title: {raw_title}
Content / Snippet: {text_snippet[:1500]}

Extract the following in strict JSON format:
{{
  "is_official": true,
  "is_current_session": true,
  "academic_year": "2025-2026",
  "dates": {{
    "form_start_date": "YYYY-MM-DD or empty",
    "form_last_date": "YYYY-MM-DD or empty",
    "admit_card_date": "YYYY-MM-DD or empty",
    "exam_date": "YYYY-MM-DD or empty"
  }},
  "summary_hindi": "2-3 short sentences student-friendly Hindi summary",
  "youtube_metadata": {{
    "title": "Viral YouTube Title in Hindi+English with Sagar Sir",
    "tags": ["tag1", "tag2"]
  }}
}}

Important: If the notice is clearly from an old previous year (e.g., 2023 or 2024), set "is_current_session": false.
"""

    try:
        resp = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        print(f"AI Analysis Error: {e}")
        return {
            "is_official": True,
            "is_current_session": True,
            "academic_year": "2025-2026",
            "dates": {},
            "summary_hindi": raw_title,
            "youtube_metadata": {
                "title": f"{raw_title} | Sagar Coaching Centre",
                "tags": ["exam notice", "sagar coaching"]
            }
        }
