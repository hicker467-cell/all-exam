import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_key)

sample_notice_text = """
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
    "form_start_date": "YYYY-MM-DD",
    "form_last_date": "YYYY-MM-DD",
    "admit_card_date": "YYYY-MM-DD",
    "exam_date": "YYYY-MM-DD"
  }},
  "summary_hindi": "2-3 sentences student-friendly Hindi summary",
  "youtube_metadata": {{
    "title": "Viral YouTube Title in Hindi+English",
    "tags": ["tag1", "tag2"]
  }}
}}

Notice Text:
{sample_notice_text}
"""

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    print("Groq AI Response:")
    print(response.choices[0].message.content)
except Exception as e:
    print("Groq AI Error:", e)
