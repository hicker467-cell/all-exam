import os
import requests
import json
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, COACHING_YOUTUBE

def send_telegram_alert(notice_data: dict, screenshot_path: str = None) -> bool:
    """
    Sends formatted Hindi exam notice with YouTube metadata, advance alert badges,
    and screenshot to personal Telegram.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram bot credentials missing in config.")
        return False
        
    dates = notice_data.get("dates", {})
    yt = notice_data.get("youtube_metadata", {})
    alert_type = notice_data.get("alert_type", "LIVE_UPDATE")
    
    dates_lines = []
    if dates.get("form_start_date"):
        dates_lines.append(f"🟢 <b>आवेदन शुरू:</b> {dates['form_start_date']}")
    if dates.get("form_last_date"):
        dates_lines.append(f"🔴 <b>अंतिम तिथि:</b> {dates['form_last_date']}")
    if dates.get("admit_card_date"):
        dates_lines.append(f"🟡 <b>एडमिट कार्ड:</b> {dates['admit_card_date']}")
    if dates.get("exam_date"):
        dates_lines.append(f"🔵 <b>परीक्षा तिथि:</b> {dates['exam_date']}")
        
    dates_block = "\n".join(dates_lines) if dates_lines else "🗓️ <i>तारीखें आधिकारिक नोटिस में देखें</i>"
    
    # Header badge based on Advance Alert vs Live Notice
    if alert_type == "ADVANCE_NOTICE":
        header_block = (
            "🟡 <b>[अग्रिम सूचना / UPCOMING ADVANCE ALERT]</b>\n"
            "⚠️ <i>यह आधिकारिक मीडिया द्वारा पूर्व सूचना है। लिंक निर्धारित तिथि पर एक्टिव होगा।</i>"
        )
    else:
        header_block = "🟢 <b>[लाइव सूचना / OFFICIAL NOTICE]</b>"
    
    caption = (
        f"{header_block}\n\n"
        f"🎯 <b>परीक्षा:</b> {notice_data.get('title', '')}\n"
        f"🏛️ <b>बोर्ड/स्रोत:</b> {notice_data.get('source_name', '')}\n\n"
        f"📝 <b>विवरण:</b>\n{notice_data.get('summary_hindi', '')}\n\n"
        f"📅 <b>महत्वपूर्ण तिथियां:</b>\n{dates_block}\n\n"
        f"🎬 <b>YouTube Title Suggestion:</b>\n<code>{yt.get('title', '')}</code>"
    )
    
    buttons = []
    direct_link = notice_data.get("link")
    if direct_link:
        buttons.append([{"text": "📄 ऑफिशियल नोटिस / खबर लिंक", "url": direct_link}])
    buttons.append([{"text": "📺 सागर कोचिंग YouTube चैनल", "url": COACHING_YOUTUBE}])
    
    reply_markup = json.dumps({"inline_keyboard": buttons})
    
    # 1. Try sending Photo if screenshot exists
    if screenshot_path and os.path.exists(screenshot_path):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        try:
            with open(screenshot_path, "rb") as photo:
                r = requests.post(
                    url,
                    data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024], "parse_mode": "HTML", "reply_markup": reply_markup},
                    files={"photo": photo},
                    timeout=25
                )
                if r.json().get("ok"):
                    print("Telegram Photo Alert Sent Successfully!")
                    return True
        except Exception as e:
            print(f"Error sending photo alert: {e}, falling back to text message...")
            
    # 2. Fallback to regular text sendMessage
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID, "text": caption, "parse_mode": "HTML", "reply_markup": reply_markup},
            timeout=15
        )
        ok = r.json().get("ok", False)
        if ok:
            print("Telegram Text Alert Sent Successfully!")
        return ok
    except Exception as e:
        print(f"Error sending text alert: {e}")
        return False
