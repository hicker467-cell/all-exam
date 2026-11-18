import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://bceceboard.bihar.gov.in"

def scrape_bceceb_bihar() -> list:
    """
    Scrapes Bihar Combined Entrance Competitive Examination Board (BCECEB):
    - DCECE (Polytechnic Engineering PE / Paramedical PMM & PM)
    - ITICAT (ITI Entrance)
    - BCECE (B.Sc Nursing / Agriculture / Pharmacy)
    Strictly filters out old archive years (2024, 2023, etc.).
    """
    html = fetch_html(URL, timeout=18)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    notices = []
    
    keywords = ["dcece", "pe", "pmm", "pm", "iticat", "iti", "polytechnic", "nursing", "counselling", "admit card", "allotment"]
    
    for a in soup.find_all("a", href=True):
        text = a.get_text().strip()
        href = a["href"].strip()
        text_lower = text.lower()
        href_lower = href.lower()
        
        # Skip old years
        if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', text_lower):
            continue
            
        if any(k in text_lower or k in href_lower for k in keywords):
            if len(text) > 15:
                full_url = href if href.startswith("http") else URL.rstrip("/") + "/" + href.lstrip("/")
                notices.append({
                    "exam_id": "bceceb_technical_bihar",
                    "source_name": "बिहार संयुक्त प्रवेश पर्षद (BCECEB)",
                    "title": text,
                    "link": full_url,
                    "snippet": text
                })
                if len(notices) >= 3:
                    break
                    
    return notices
