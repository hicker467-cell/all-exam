import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://medhasoft.bihar.gov.in"

def scrape_medhasoft() -> list:
    """
    Scrapes Medhasoft Bihar:
    - Mukhyamantri Balak/Balika 10th Protsahan Yojana (₹10,000)
    - Mukhyamantri Kanya Utthan 12th Inter (₹25,000)
    Strictly filters out old archive years (2024, 2023, etc.).
    """
    html = fetch_html(URL, timeout=12)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    notices = []
    
    keywords = ["protsahan", "kanya", "utthan", "medha", "बालक", "बालिका", "प्रोत्साहन", "कन्या उत्थान", "आवेदन", "scholarship"]
    
    for a in soup.find_all("a", href=True):
        text = a.get_text().strip()
        href = a["href"].strip()
        text_lower = text.lower()
        href_lower = href.lower()
        
        # Skip old years
        if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', text_lower):
            continue
            
        if any(k in text_lower or k in href_lower for k in keywords):
            if len(text) > 10:
                full_url = href if href.startswith("http") else URL.rstrip("/") + "/" + href.lstrip("/")
                notices.append({
                    "exam_id": "medhasoft_scholarship_bihar",
                    "source_name": "मेधासॉफ्ट छात्रवृत्ति (शिक्षा विभाग, बिहार)",
                    "title": text,
                    "link": full_url,
                    "snippet": text
                })
                if len(notices) >= 2:
                    break
                    
    return notices
