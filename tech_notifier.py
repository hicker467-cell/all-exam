import json
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_tech_telegram_alert(tech_data: dict) -> bool:
    """
    Sends a formatted Telegram alert specifically for the 'Coding with Sudhir' channel.
    Clearly distinguishes from Sagar Coaching Centre alerts.
    Includes the YouTube title, direct download link, and screen recording blueprint.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram bot credentials missing in config.")
        return False

    tool_name = tech_data.get("tool_name", "Tech Update")
    category = tech_data.get("category", "Software Release")
    why_viral = tech_data.get("why_viral", "")
    yt_title = tech_data.get("youtube_title", "")
    duration = tech_data.get("target_duration", "2.5 Minutes")
    steps = tech_data.get("screen_recording_blueprint", [])
    hindi_tip = tech_data.get("hindi_tip_for_sudhir", "")
    direct_link = tech_data.get("link", "")
    release_badge = tech_data.get("release_badge", "🟢 FRESH")
    
    steps_formatted = ""
    for idx, step in enumerate(steps, 1):
        steps_formatted += f"<b>{idx}.</b> {step}\n"
    if not steps_formatted:
        steps_formatted = "1. Download official setup\n2. Run installer (check PATH)\n3. Verify in CMD\n"

    message = (
        f"💻 <b>[CODING WITH SUDHIR] NEW TECH RADAR</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 <b>Status:</b> {release_badge}\n"
        f"🏷️ <b>Category:</b> {category}\n"
        f"📦 <b>Tool:</b> {tool_name}\n\n"
        f"🔥 <b>Demand / Trend:</b>\n<i>{why_viral}</i>\n\n"
        f"🎬 <b>YouTube Title Suggestion:</b>\n"
        f"<code>{yt_title}</code>\n\n"
        f"⏱️ <b>Target Length:</b> {duration}\n\n"
        f"📋 <b>Screen Recording Blueprint (Sudhir Bhai ke liye):</b>\n"
        f"{steps_formatted}\n"
        f"💡 <b>Tip:</b> {hindi_tip}\n\n"
        f"⚡ <i>Agar fresh hai to turant 2-3 min record kar lo, late ho to skip kar sakte ho!</i>"
    )

    buttons = []
    if direct_link:
        buttons.append([{"text": "🌐 Direct Download / Official Link", "url": direct_link}])

    reply_markup = json.dumps({"inline_keyboard": buttons}) if buttons else None

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            print(f"✅ Telegram alert delivered for '{tool_name}' (Coding with Sudhir)")
            return True
        else:
            print(f"⚠️ Telegram API error {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print(f"Failed to send Telegram tech alert: {e}")
        return False
