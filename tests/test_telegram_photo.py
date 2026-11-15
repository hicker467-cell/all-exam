import requests

token = "8805183217:AAEiiqSLd-yCXhTDqr37BFFGZ-06QIOcWG8"
chat_id = "1479947858"
photo_path = "screenshots/navodaya_test.png"

url = f"https://api.telegram.org/bot{token}/sendPhoto"
caption = (
    "📸 <b>लाइव टेस्ट स्क्रीनशॉट: नवोदय विद्यालय समिति</b>\n\n"
    "✅ <b>स्टेटस:</b> Playwright Headless Browser द्वारा लाइव कैप्चर किया गया।\n"
    "🏫 <b>पोर्टल:</b> navodaya.gov.in (React SPA)\n"
    "🎯 <b>परिणाम:</b> असली सरकारी पेज बिना किसी एरर के सफलतापूर्वक पढ़ा गया!"
)

with open(photo_path, "rb") as f:
    r = requests.post(
        url,
        data={"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"},
        files={"photo": f},
        timeout=25
    )

print("Telegram Photo Response:", r.json())
