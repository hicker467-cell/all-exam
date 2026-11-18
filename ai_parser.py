import json
from datetime import datetime
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
    Uses Groq AI to extract structured dates, verify authenticity,
    filter out irrelevant jobs or past expired events,
    and generate student-friendly Hindi summary and YouTube metadata.
    """
    client = get_ai_client()
    today_str = datetime.now().strftime("%Y-%m-%d")
    current_year = datetime.now().year
    
    prompt = f"""
You are the Chief Exam & Scholarship Analyst for Sagar Coaching Centre (Bhagwanpur).
Today's Date: {today_str}
Current Academic Sessions: {current_year}-{current_year + 1} and {current_year + 1}-{current_year + 2}.

TARGET AUDIENCE:
Class 1 to 12 students in Hindi belt (Bihar, UP, MP, Rajasthan, Jharkhand, etc.).
TARGET EXAMS:
1. NMMS Scholarship (Class 8)
2. Navodaya Vidyalaya (JNVST Class 6 & 9)
3. Sainik School (AISSEE Class 6 & 9)
4. Sir CV Raman Science Talent & Ramanujan Maths Talent Search (Class 6-12)
5. Atal Awasiya Vidyalaya (Class 6 & 9)
6. Simultala Awasiya Vidyalaya (SAV Class 6)
7. State Boards: BSEB Matric & Inter (10th/12th), UPMSP (10th/12th)
8. Polytechnic (DCECE / JEECUP) & ITICAT (Class 10 level)
9. State Scholarships: Medhasoft (Bihar Class 1-12, Kanya Utthan ₹25,000, Balak/Balika ₹10,000)
10. PM Yashasvi & SHRESHTA

IRRELEVANT TOPICS TO REJECT:
- Adult jobs (UPSC, BPSC Civil, SSC CGL/CHSL, Police Constable, Daroga, Bank PO, Railway Group D, AIBE, NEET PG, UGC NET)
- General articles, interview schedules, motivational stories, unrelated news.
- Any notice from past years (2023, 2024, or 2024-25) or whose deadlines have already passed prior to {today_str}.

Analyze this notice from source '{source_name}':
Title: {raw_title}
Content / Snippet: {text_snippet[:1500]}

Return STRICT JSON ONLY:
{{
  "is_target_exam": true or false,
  "is_active_future_event": true or false,
  "rejection_reason": "Explanation if false, else empty",
  "academic_year": "{current_year}-{current_year + 1}",
  "dates": {{
    "form_start_date": "YYYY-MM-DD or empty",
    "form_last_date": "YYYY-MM-DD or empty",
    "admit_card_date": "YYYY-MM-DD or empty",
    "exam_date": "YYYY-MM-DD or empty"
  }},
  "summary_hindi": "2-3 short, clear sentences in Hindi for students and parents",
  "youtube_metadata": {{
    "title": "Viral YouTube Video Title in Hindi+English (e.g., Exam Name Form 2026 Kab Aayega? By Sagar Sir)",
    "tags": ["exam notice", "sagar coaching centre"]
  }}
}}
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
            "is_target_exam": True,
            "is_active_future_event": True,
            "rejection_reason": "",
            "academic_year": f"{current_year}-{current_year + 1}",
            "dates": {},
            "summary_hindi": raw_title,
            "youtube_metadata": {
                "title": f"{raw_title} | Sagar Coaching Centre",
                "tags": ["exam notice", "sagar coaching"]
            }
        }
