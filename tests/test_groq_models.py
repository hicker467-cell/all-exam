import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

sample_text = """
बिहार विद्यालय परीक्षा समिति, पटना
विज्ञप्ति संख्या PR 215/2025
राष्ट्रीय आय-सह-मेधा छात्रवृत्ति योजना (NMMS) 2025-26 के लिए ऑनलाइन आवेदन आमंत्रित किए जाते हैं।
आवेदन प्रारम्भ होने की तिथि: 10 दिसंबर 2025
ऑनलाइन आवेदन भरने की अंतिम तिथि: 31 दिसंबर 2025
प्रवेश पत्र (Admit Card) जारी करने की तिथि: 12 जनवरी 2026
परीक्षा की तिथि: 25 जनवरी 2026
छात्रवृत्ति राशि: ₹12,000 प्रति वर्ष (कुल ₹48,000)।
विस्तृत जानकारी वेबसाइट https://scert.bihar.gov.in पर उपलब्ध है।
"""

prompt = f"""
You are an expert Indian exam notification analyzer for Sagar Coaching Centre.
Analyze this official notice text and return strictly valid JSON matching this schema:
{{
  "is_official": true,
  "exam_name": "NMMS Bihar 2025-26",
  "academic_year": "2025-2026",
  "press_release_no": "PR 215/2025",
  "dates": {{
    "form_start_date": "2025-12-10",
    "form_last_date": "2025-12-31",
    "admit_card_date": "2026-01-12",
    "exam_date": "2026-01-25"
  }},
  "summary_hindi": "बिहार NMMS 2025-26 का फॉर्म 10 से 31 दिसंबर तक भरा जाएगा...",
  "youtube_metadata": {{
    "title": "Bihar NMMS 2025-26 Form Kaise Bhare | Step-by-Step | Sagar Sir",
    "tags": ["nmms bihar 2025", "sagar coaching"]
  }}
}}

Notice Text:
{sample_text}
"""

for model in ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]:
    try:
        print(f"Testing Model: {model}...")
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        print(f"SUCCESS with {model}!")
        print(resp.choices[0].message.content)
        break
    except Exception as e:
        print(f"Failed {model}:", e)
