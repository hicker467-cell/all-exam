import time
import os
import sys

# Ensure current directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import generate_tech_dedup_hash, is_tech_duplicate, save_tech_notification
from ai_tech_parser import analyze_tech_update
from tech_notifier import send_tech_telegram_alert
from scrapers.tech_radar import scrape_all_tech
from content_extractor import extract_content_from_link

def process_tech_item(item: dict, dry_run: bool = False):
    tool_id = item.get("tool_id", "")
    version_tag = item.get("version_tag", "")
    title = item.get("title", "")
    link = item.get("link", "")
    content = item.get("content_snippet", "")
    update_type = item.get("update_type", "Software Release")
    
    print(f"\n🔎 [TECH SCAN] Checking: {title} ({version_tag})", flush=True)
    
    # 1. Deduplication Check
    dedup_hash = generate_tech_dedup_hash(tool_id, version_tag, link=link, title=title)
    if is_tech_duplicate(dedup_hash, link=link, title=title):
        print(f"⏩ [ALREADY SENT] {title} previously notified. Skipping.", flush=True)
        return False
        
    # Lazy content extraction if snippet is empty
    if not content and link:
        print(f"📥 [EXTRACTING ARTICLE] Fetching article content from {link[:50]}...", flush=True)
        content = extract_content_from_link(link, timeout=8)
        
    # 2. AI Analysis using Groq
    print(f"🤖 [AI EVALUATING] Analyzing with Groq AI for 'Coding with Sudhir' blueprint...", flush=True)
    ai_result = analyze_tech_update(title, content, link, update_type)
    
    if not ai_result.get("is_worthy_for_video", True):
        print(f"🛑 [LOW PRIORITY] AI decided this is not worth a video right now.", flush=True)
        return False
        
    payload = {
        "tool_id": tool_id,
        "version_tag": version_tag,
        "dedup_hash": dedup_hash,
        "title": title,
        "tool_name": ai_result.get("tool_name", title),
        "category": ai_result.get("category", update_type),
        "release_badge": item.get("release_badge", "🟢 FRESH"),
        "why_viral": ai_result.get("why_viral", ""),
        "youtube_title": ai_result.get("youtube_title", f"How to Install {title} on Windows 11"),
        "target_duration": ai_result.get("target_duration", "2.5 Minutes"),
        "screen_recording_blueprint": ai_result.get("screen_recording_blueprint", []),
        "hindi_tip_for_sudhir": ai_result.get("hindi_tip_for_sudhir", ""),
        "youtube_tags": ai_result.get("youtube_tags", []),
        "link": link
    }
    
    if dry_run:
        print("\n" + "=" * 50, flush=True)
        print("🎯 [DRY RUN PREVIEW - CODING WITH SUDHIR]", flush=True)
        print("=" * 50, flush=True)
        print(f"📦 Tool Name:    {payload['tool_name']}", flush=True)
        print(f"🎬 YouTube Title: {payload['youtube_title']}", flush=True)
        print(f"⏱️ Duration:     {payload['target_duration']}", flush=True)
        print(f"🔥 Why Viral:    {payload['why_viral']}", flush=True)
        print(f"📋 Blueprint:", flush=True)
        for i, step in enumerate(payload['screen_recording_blueprint'], 1):
            print(f"   {i}. {step}", flush=True)
        print(f"💡 Hindi Tip:    {payload['hindi_tip_for_sudhir']}", flush=True)
        print(f"🔗 Link:         {payload['link']}", flush=True)
        print("=" * 50 + "\n", flush=True)
        return True
        
    # 3. Send Telegram Alert to Sudhir
    print(f"🚀 [SENDING ALERT] Dispatching to Telegram...", flush=True)
    delivered = send_tech_telegram_alert(payload)
    
    # 4. Save to Database
    if delivered:
        save_tech_notification(payload)
        print(f"💾 [SAVED] Tech update recorded in MongoDB.", flush=True)
        return True
    return False

def run_tech_radar(dry_run: bool = False, max_alerts: int = 1):
    print("=" * 65, flush=True)
    print("🚀 Coding with Sudhir - Tech & AI Release Radar Engine", flush=True)
    print("=" * 65, flush=True)
    
    items = scrape_all_tech()
    print(f"Found {len(items)} total candidate tech updates.", flush=True)
    
    processed = 0
    for item in items:
        if processed >= max_alerts:
            print(f"Reached max limit of {max_alerts} alerts for this scan.", flush=True)
            break
        try:
            success = process_tech_item(item, dry_run=dry_run)
            if success:
                processed += 1
                time.sleep(1)
        except Exception as e:
            print(f"Error processing {item.get('title')}: {e}", flush=True)
            
    print("\n" + "=" * 65, flush=True)
    print(f"🎉 Radar Scan Complete! Sent {processed} alerts.", flush=True)
    print("=" * 65, flush=True)

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    run_tech_radar(dry_run=is_dry, max_alerts=1)
