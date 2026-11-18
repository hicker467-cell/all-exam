from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://secondary.biharboardonline.com"

def scrape_bseb_bihar() -> list:
    """
    Scrapes Bihar School Examination Board (BSEB):
    - Matric (Class 10th)
    - Inter (Class 12th)
    - Simultala Awasiya Vidyalaya (SAV Class 6)
    - Olympiad & Crossword
    """
    html = fetch_html(URL, timeout=15)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    notices = []
    
    keywords = ["matric", "inter", "simultala", "sav", "विज्ञप्ति", "admit", "result", "time table", "ओलंपियाड", "क्रॉसवर्ड"]
    
    for a in soup.find_all("a", href=True):
        text = a.get_text().strip()
        href = a["href"].strip()
        text_lower = text.lower()
        href_lower = href.lower()
        
        if any(k in text_lower or k in href_lower for k in keywords):
            if len(text) > 10:
                full_url = href if href.startswith("http") else URL.rstrip("/") + "/" + href.lstrip("/")
                notices.append({
                    "exam_id": "bseb_bihar_board",
                    "source_name": "बिहार बोर्ड (BSEB Patna)",
                    "title": text,
                    "link": full_url,
                    "snippet": text
                })
                if len(notices) >= 3:
                    break
                    
    return notices
