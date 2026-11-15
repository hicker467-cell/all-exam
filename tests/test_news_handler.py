import time
import requests
import json
from bs4 import BeautifulSoup
from config import BROWSER_HEADERS
from content_extractor import extract_content_from_link
from ai_parser import get_ai_client, AI_MODEL
from screenshot import capture_screenshot
from notifier import send_telegram_alert
from database import generate_dedup_hash, is_duplicate, save_notification

def classify_and_parse_news(title: str, text: str, source_name: str) -> dict:
    """
    Dedicated AI prompt for News Portals (Hindustan, Jagran, Prabhat Khabar).
    Filters out motivational stories, tips, and clickbait.
    Extracts only genuine exam/admission/scholarship notices with verified deadlines.
    """
    client = get_ai_client()
    
    prompt = f"""
You are a senior news editor and exam analyst for Sagar Coaching Centre.
Analyze this news article from '{source_name}':
Title: {title}
Body Text: {text[:2500]}

Your task is to classify this news and extract details strictly in JSON:
{{
  "is_exam_notification": true,         // true ONLY for exams, admissions, scholarship, recruitment notices. False for success stories, motivational blogs, general tips.
  "notice_type": "DATE_EXTENSION or FORM_START or ADMIT_CARD or RESULT or GENERAL_JOB",
  "exam_or_recruitment_name": "Exact Name of Exam or Scheme",
  "target_audience": "10th pass / 12th pass / Class 6 / Class 8 etc.",
  "is_current_session": true,           // false if it refers to old 2023/2024 sessions
  "dates": {{
    "form_start_date": "YYYY-MM-DD or empty",
    "form_last_date": "YYYY-MM-DD (Key Deadline) or empty",
    "admit_card_date": "YYYY-MM-DD or empty",
    "exam_date": "YYYY-MM-DD or empty"
  }},
  "summary_hindi": "2-3 short, clear sentences in Hindi explaining what students need to know and the deadline.",
  "youtube_metadata": {{
    "title": "Viral YouTube Title for Sagar Sir (Hindi + English)",
    "tags": ["tag1", "tag2"]
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
        print(f"News AI Parsing Error: {e}")
        return {"is_exam_notification": False}

def test_live_news_handler():
    print("=" * 70)
    print("📰 TESTING LIVE NEWSPAPER HANDLER (HINDUSTAN & PRABHAT KHABAR)")
    print("=" * 70)
    
    # 1. Fetch live articles from Live Hindustan
    url = "https://www.livehindustan.com/career/"
    resp = requests.get(url, headers=BROWSER_HEADERS, verify=False, timeout=12)
    soup = BeautifulSoup(resp.text, "html.parser")
    
    candidates = []
    for a in soup.find_all("a", href=True):
        t = a.get_text().strip()
        h = a["href"].strip()
        if len(t) > 30 and "/career/" in h:
            full_url = h if h.startswith("http") else "https://www.livehindustan.com" + h
            if full_url not in [c["url"] for c in candidates]:
                candidates.append({"title": t, "url": full_url})
                if len(candidates) >= 5:
                    break
                    
    print(f"Found {len(candidates)} Live Headlines to evaluate.\n")
    
    for idx, item in enumerate(candidates, 1):
        t = item["title"]
        u = item["url"]
        print(f"\n--- [HEADLINE {idx}] ---")
        print(f"Title: {t}")
        print(f"URL: {u}")
        
        # Extract full article text
        article_text = extract_content_from_link(u)
        print(f"Article Body Extracted: {len(article_text)} characters")
        
        # AI Classification & Parsing
        parsed = classify_and_parse_news(t, article_text, "लाइव हिन्दुस्तान")
        
        is_notice = parsed.get("is_exam_notification", False)
        print(f"Is Genuine Exam Notification?: {is_notice}")
        
        if not is_notice:
            print("❌ [FILTERED OUT] Skipped (Motivational story / General tip / Non-exam content).")
            continue
            
        print("✅ [APPROVED] Genuine Exam Notice Detected!")
        print(f"   Exam Name: {parsed.get('exam_or_recruitment_name')}")
        print(f"   Dates: {parsed.get('dates')}")
        print(f"   Summary: {parsed.get('summary_hindi')}")
        print(f"   Suggested YouTube Title: {parsed.get('youtube_metadata', {}).get('title')}")
        
        # Check Deduplication
        exam_id = "news_" + "".join(c for c in parsed.get("exam_or_recruitment_name", "news").lower() if c.isalnum())[:15]
        d_hash = generate_dedup_hash(exam_id, t, u, parsed.get("dates"))
        
        if is_duplicate(d_hash):
            print("⏩ [DUPLICATE] Already in MongoDB. Skipping duplicate alert.")
            continue
            
        # Capture Screenshot
        print("📸 Capturing Article Screenshot with Playwright...")
        scr_path = capture_screenshot(u, f"news_{idx}_{int(time.time())}")
        
        # Prepare Document & Save
        doc = {
            "exam_id": exam_id,
            "source_name": "लाइव हिन्दुस्तान (शिक्षा समाचार)",
            "title": t,
            "link": u,
            "dedup_hash": d_hash,
            "academic_year": parsed.get("academic_year", "2025-2026"),
            "dates": parsed.get("dates", {}),
            "summary_hindi": parsed.get("summary_hindi", t),
            "youtube_metadata": parsed.get("youtube_metadata", {}),
            "screenshot_path": scr_path
        }
        save_notification(doc)
        print("💾 Saved to MongoDB.")
        
        # Send Telegram Alert
        print("🚀 Sending Live News Alert to Telegram...")
        send_telegram_alert(doc, scr_path)
        print("Telegram alert delivered successfully!\n")
        break # Test 1 genuine article fully end-to-end

if __name__ == "__main__":
    test_live_news_handler()
