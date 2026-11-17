import os
import sys
import time
from database import generate_dedup_hash, is_duplicate, save_notification
from ai_parser import analyze_notice
from screenshot import capture_screenshot
from notifier import send_telegram_alert
from content_extractor import extract_content_from_link

from scrapers.cv_raman import scrape_cv_raman
from scrapers.nmms_bihar import scrape_nmms_bihar
from scrapers.navodaya import scrape_navodaya
from scrapers.newspapers import scrape_newspapers
from tech_radar_runner import run_tech_radar

def process_notice(item: dict):
    exam_id = item.get("exam_id", "general_exam")
    title = item.get("title", "")
    link = item.get("link", "")
    source_name = item.get("source_name", "Official Board")
    
    print(f"\n[FOUND] {title[:70]}... ({source_name})")
    
    # 1. Quick Deduplication Check (Layer 1)
    temp_hash = generate_dedup_hash(exam_id, title, link)
    if is_duplicate(temp_hash):
        print(f"⏩ [DUPLICATE] Already in MongoDB. Skipping.")
        return False
        
    # 2. Extract Deep Content (PDF / HTML Article)
    print(f"📥 [EXTRACTING CONTENT] Reading circular/article body...")
    body_text = extract_content_from_link(link)
    content_to_analyze = body_text if len(body_text) > 100 else title
    
    # 3. Analyze with Groq AI (Llama/GPT-OSS)
    print(f"🤖 [AI PARSING] Analyzing with Groq AI for dates & summary...")
    ai_data = analyze_notice(title, content_to_analyze, source_name)
    
    # 4. Check Previous Year Filter
    if not ai_data.get("is_current_session", True):
        print(f"🛑 [OLD NOTICE] Detected old archive year. Skipping.")
        return False
        
    dates = ai_data.get("dates", {})
    print(f"📅 Extracted Dates: {dates}")
    
    # 5. Final Deduplication Hash with Key Date
    final_hash = generate_dedup_hash(exam_id, title, link, dates)
    if is_duplicate(final_hash):
        print(f"⏩ [DUPLICATE] Final hash match in MongoDB. Skipping.")
        return False
        
    # 6. Capture Live Screenshot
    print(f"📸 [SCREENSHOT] Capturing headless browser snapshot...")
    screenshot_path = capture_screenshot(link, f"{exam_id}_{int(time.time())}")
    if screenshot_path:
        print(f"✅ Screenshot saved: {screenshot_path}")
    else:
        print(f"⚠️ Screenshot skipped (direct file or timeout).")
        
    # 7. Prepare and Save Document
    doc = {
        "exam_id": exam_id,
        "source_name": source_name,
        "title": title,
        "link": link,
        "dedup_hash": final_hash,
        "academic_year": ai_data.get("academic_year", "2025-2026"),
        "dates": dates,
        "summary_hindi": ai_data.get("summary_hindi", title),
        "youtube_metadata": ai_data.get("youtube_metadata", {}),
        "screenshot_path": screenshot_path
    }
    
    saved = save_notification(doc)
    if saved:
        print(f"💾 [SAVED] Document inserted into MongoDB 'notifications' collection.")
    else:
        print(f"⚠️ Failed saving to MongoDB.")
        return False
        
    # 8. Broadcast to Telegram Personal Chat
    print(f"🚀 [TELEGRAM] Sending alert to personal chat...")
    send_telegram_alert(doc, screenshot_path)
    return True

def run_all_scrapers():
    print("=" * 65)
    print("🌟 Sagar Coaching Centre - Full Exam Notification & AI Engine")
    print("=" * 65)
    
    scrapers = [
        ("सर सी.वी. रमन टैलेंट सर्च (BCST)", scrape_cv_raman),
        ("NMMS बिहार (SCERT)", scrape_nmms_bihar),
        ("नवोदय विद्यालय (JNVST)", scrape_navodaya),
        ("लाइव हिन्दुस्तान शिक्षा समाचार", scrape_newspapers)
    ]
    
    total_processed = 0
    for name, scraper_fn in scrapers:
        print(f"\n🔎 Checking Source: {name}...")
        try:
            items = scraper_fn()
            print(f"Found {len(items)} items from {name}")
            for item in items[:3]: # top 3 most recent per source
                processed = process_notice(item)
                if processed:
                    total_processed += 1
                time.sleep(1)
        except Exception as e:
            print(f"Error running scraper {name}: {e}")
            
    print("\n" + "=" * 65)
    print(f"🎉 Exam Run Complete! New Verified Notices Broadcasted: {total_processed}")
    print("=" * 65)
    
    # Run Tech & AI Release Radar for 'Coding with Sudhir'
    print("\n" + "=" * 65)
    print("🚀 Launching Coding with Sudhir - Tech & AI Release Radar")
    print("=" * 65)
    try:
        run_tech_radar(max_alerts=3)
    except Exception as e:
        print(f"Error running Tech Radar: {e}")

if __name__ == "__main__":
    run_all_scrapers()
