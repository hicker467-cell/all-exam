import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://scert.bihar.gov.in"

def scrape_nmms_bihar() -> list:
    """
    Scrapes NMMS (National Means-cum-Merit Scholarship) and NTSE notices from SCERT Bihar.
    Strictly filters out old archive years (2024-25, 2023, etc.) and past result sheets.
    """
    html = fetch_html(URL, timeout=20)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    notices = []
    
    for link in soup.find_all("a", href=True):
        text = link.get_text().strip()
        href = link["href"].strip()
        text_lower = text.lower()
        href_lower = href.lower()
        
        # 1. Skip old year archives
        if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', text_lower):
            continue
            
        # 2. Check for NMMS keywords
        keywords = ["nmms", "nmmss", "राष्ट्रीय साधन", "मेधा छात्रवृत्ति", "scert notification"]
        if any(k in text_lower or k in href_lower for k in keywords):
            full_url = href if href.startswith("http") else URL + (href if href.startswith("/") else "/" + href)
            notices.append({
                "exam_id": "bihar_nmms",
                "source_name": "SCERT बिहार",
                "title": text or "SCERT Bihar NMMS Notice",
                "link": full_url,
                "snippet": text
            })
            
    return notices
