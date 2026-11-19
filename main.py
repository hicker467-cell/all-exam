import os
import sys
import time
import re
from datetime import datetime
from database import generate_dedup_hash, is_duplicate, save_notification
from ai_parser import analyze_notice
from screenshot import capture_screenshot
from notifier import send_telegram_alert
from content_extractor import extract_content_from_link

# Import all active exam scrapers
from scrapers.cv_raman import scrape_cv_raman
from scrapers.nmms_bihar import scrape_nmms_bihar
from scrapers.navodaya import scrape_navodaya
from scrapers.atal_awasiya import scrape_atal_awasiya
from scrapers.nta_exams import scrape_nta_exams
from scrapers.nmms_multistate import scrape_nmms_multistate
from scrapers.bseb_bihar import scrape_bseb_bihar
from scrapers.bceceb_bihar import scrape_bceceb_bihar
from scrapers.medhasoft import scrape_medhasoft
from scrapers.up_exams import scrape_up_exams
from scrapers.newspapers import scrape_newspapers

# Tech & AI radar for Coding with Sudhir
from tech_radar_runner import run_tech_radar

GENERIC_NAV_TITLES = [
    "scholarship portal", "portal", "examination result", "citizen home",
    "competitive examinations", "home", "contact us", "about us", "download",
    "important links", "latest updates", "notice board", "nmmss", "nmms",
    "science technology and technical education department"
]

def is_valid_date_format(d_str: str) -> bool:
    try:
        datetime.strptime(d_str.strip(), "%Y-%m-%d")
        return True
    except (ValueError, TypeError, AttributeError):
        return False

def validate_date_and_relevance(item: dict, ai_data: dict) -> tuple[bool, str]:
    today = datetime.now().date()
    title = item.get("title", "")
    t_lower = title.lower()
    exam_id = item.get("exam_id", "")
    is_newspaper = (exam_id == "hindi_newspaper_alert")
    
    # 1. Clean title check against generic menu/nav buttons
    clean_t = re.sub(r'[^a-zA-Z0-9\s]', '', t_lower).strip()
    if clean_t in GENERIC_NAV_TITLES:
        return False, f"Generic website navigation link ({title[:50]})"
        
    words = [w for w in re.split(r'\s+', clean_t) if w]
    if len(words) <= 2 and not any(k in t_lower for k in ["2026", "2027", "2028"]):
        return False, f"Non-descriptive short navigation text ({title[:50]})"
        
    # 2. Regex check for old archive years (2020-2024, 2024-25, 2023-24)
    if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', t_lower):
        return False, f"Old academic year in title ({title[:50]})"
        
    # 3. Check Blacklisted Irrelevant topics (UPSC, adult jobs, police, clickbait)
    blacklisted = [
        "upsc", "bpsc", "constable", "कांस्टेबल", "police", "दरोगा", 
        "ड्राइवर", "कहानी", "interview schedule", "इंटरव्यू", "aibe", "bar council",
        "civil judge", "ugc net", "neet pg"
    ]
    if any(b in t_lower for b in blacklisted):
        return False, f"Irrelevant non-school topic ({title[:50]})"
        
    # 4. AI Target Exam Check
    if not ai_data.get("is_target_exam", True):
        reason = ai_data.get("rejection_reason", "Not relevant to Class 1-12 coaching")
        return False, f"AI Target Filter: {reason}"
        
    if not ai_data.get("is_active_future_event", True):
        reason = ai_data.get("rejection_reason", "Past/expired event")
        return False, f"AI Date Filter: {reason}"
        
    # 5. Strict Deterministic Date Verification
    dates = ai_data.get("dates", {})
    last_date_str = dates.get("form_last_date", "").strip() if dates else ""
    exam_date_str = dates.get("exam_date", "").strip() if dates else ""
    admit_date_str = dates.get("admit_card_date", "").strip() if dates else ""
    start_date_str = dates.get("form_start_date", "").strip() if dates else ""
    
    # Check if form_last_date is strictly in the past
    if last_date_str and is_valid_date_format(last_date_str):
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
        if last_date < today:
            if exam_date_str and is_valid_date_format(exam_date_str):
                exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
                if exam_date < today:
                    return False, f"Expired: Form closed on {last_date_str} & exam was on {exam_date_str}"
            else:
                return False, f"Expired: Application last date ({last_date_str}) already passed"

    # Check if exam_date is in the past
    if exam_date_str and is_valid_date_format(exam_date_str):
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        if exam_date < today:
            return False, f"Expired: Exam date ({exam_date_str}) already passed"
            
    # Check if all dates present are strictly in the past
    all_dates = [d for d in [last_date_str, exam_date_str, admit_date_str, start_date_str] if d and is_valid_date_format(d)]
    if all_dates:
        parsed_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in all_dates]
        if all(d < today for d in parsed_dates):
            return False, f"Expired: All dates {all_dates} are in the past"
            
    # 6. Safety Net for Official Government Portals vs Newspapers:
    # If it is an official portal (SCERT, Navodaya, AVS, BCST, NTA, BSEB) and AI verified it as target exam:
    # We DO NOT reject it even if exact dates are "शीघ्र घोषित" (coming soon in circular).
    # Only newspapers require mandatory future dates to prevent clickbait fluff.
    if is_newspaper and not all_dates:
        return False, "Newspaper article lacks verified future deadline dates"
        
    return True, "Valid active notice"

def process_notice(item: dict):
    exam_id = item.get("exam_id", "general_exam")
    title = item.get("title", "")
    link = item.get("link", "")
    source_name = item.get("source_name", "Official Board")
    
    if not title or not link:
        return False
        
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
    
    # 3. Analyze with Groq AI (Dates & Summary)
    print(f"🤖 [AI PARSING] Analyzing with Groq AI for dates & summary...")
    ai_data = analyze_notice(title, content_to_analyze, source_name)
    
    # 4. Strict Date & Relevance Filter
    is_valid, reason = validate_date_and_relevance(item, ai_data)
    if not is_valid:
        print(f"🛑 [FILTER REJECTED] {reason}. Skipping alert!")
        return False
        
    dates = ai_data.get("dates", {})
    print(f"📅 Verified Active Dates: {dates}")
    
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
        "alert_type": ai_data.get("alert_type", "LIVE_UPDATE"),
        "academic_year": ai_data.get("academic_year", "2026-2027"),
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
    print(f"🚀 [TELEGRAM] Sending verified active alert to personal chat...")
    send_telegram_alert(doc, screenshot_path)
    return True

def run_all_scrapers():
    print("=" * 70)
    print("🌟 Sagar Coaching Centre - Full 100+ Exam Notification Engine")
    print(f"📅 System Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # All Active Scraper Suites Covering 100+ Exams
    scrapers = [
        ("सर सी.वी. रमन टैलेंट सर्च (BCST)", scrape_cv_raman),
        ("NMMS बिहार (SCERT)", scrape_nmms_bihar),
        ("नवोदय विद्यालय प्रवेश (JNVST)", scrape_navodaya),
        ("अटल आवासीय विद्यालय (AVS / UPBOCW)", scrape_atal_awasiya),
        ("सैनिक स्कूल व PM यशस्वी (NTA)", scrape_nta_exams),
        ("NMMS मल्टी-स्टेट (UP/MP/RJ/JH/CG)", scrape_nmms_multistate),
        ("बिहार बोर्ड 10th/12th व सिमुलतला (BSEB)", scrape_bseb_bihar),
        ("बिहार पॉलिटेक्निक व ITI (BCECEB)", scrape_bceceb_bihar),
        ("मेधासॉफ्ट छात्रवृत्ति (शिक्षा विभाग)", scrape_medhasoft),
        ("UP Board, JEECUP व विद्याज्ञान (UP)", scrape_up_exams),
        ("ई-पेपर शिक्षा समाचार (हिन्दुस्तान व प्रभात खबर)", scrape_newspapers)
    ]
    
    total_processed = 0
    for name, scraper_fn in scrapers:
        print(f"\n🔎 Checking Source: {name}...")
        try:
            items = scraper_fn()
            print(f"Found {len(items)} items from {name}")
            for item in items[:2]: # top 2 active notices per portal
                processed = process_notice(item)
                if processed:
                    total_processed += 1
                time.sleep(1) # polite gap
        except Exception as e:
            print(f"Error running scraper {name}: {e}")
            
    print("\n" + "=" * 70)
    print(f"🎉 Exam Run Complete! New Verified Active Notices Broadcasted: {total_processed}")
    print("=" * 70)
    
    # Run Tech & AI Release Radar for 'Coding with Sudhir'
    print("\n" + "=" * 70)
    print("🚀 Launching Coding with Sudhir - Tech & AI Release Radar")
    print("=" * 70)
    try:
        run_tech_radar(max_alerts=3)
    except Exception as e:
        print(f"Error running Tech Radar: {e}")

if __name__ == "__main__":
    run_all_scrapers()
