from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://www.livehindustan.com/career/"

def scrape_newspapers() -> list:
    """
    Scrapes breaking exam and scholarship announcements from Live Hindustan Education.
    """
    html = fetch_html(URL, timeout=20)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    notices = []
    
    # Priority keywords for school & scholarship exams
    keywords = [
        "nmms", "रमन", "नवोदय", "सैनिक स्कूल", "सिमुलतला", "matric", "inter", 
        "admit card", "स्कॉलरशिप", "छात्रवृत्ति", "पॉलिटेक्निक", "iti", "agniveer", "कांस्टेबल"
    ]
    
    for a in soup.find_all("a", href=True):
        title = a.get_text().strip()
        href = a["href"].strip()
        
        if len(title) > 25:
            title_lower = title.lower()
            if any(k in title_lower for k in keywords):
                full_url = href if href.startswith("http") else "https://www.livehindustan.com" + href
                notices.append({
                    "exam_id": "hindi_newspaper_alert",
                    "source_name": "लाइव हिन्दुस्तान (शिक्षा समाचार)",
                    "title": title,
                    "link": full_url,
                    "snippet": title
                })
                if len(notices) >= 3:
                    break
                    
    return notices
