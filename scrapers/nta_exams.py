import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

def scrape_nta_exams() -> list:
    """
    Scrapes National Testing Agency (NTA) for active school & scholarship entrance exams:
    - Sainik School Entrance (AISSEE)
    - PM Yashasvi Scholarship (YASASVI)
    - SHRESHTA Scheme
    """
    notices = []
    
    # Check NTA Homepage Active Announcements
    html = fetch_html("https://nta.ac.in", timeout=20)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    
    targets = {
        "aissee": ("national_sainik_school", "सैनिक स्कूल प्रवेश परीक्षा (AISSEE)"),
        "sainik": ("national_sainik_school", "सैनिक स्कूल प्रवेश परीक्षा (AISSEE)"),
        "yasasvi": ("pm_yashasvi_scholarship", "PM यशस्वी छात्रवृत्ति (NTA)"),
        "shreshta": ("nta_shreshta", "श्रेष्ठ योजना (SHRESHTA NTA)")
    }
    
    for a in soup.find_all("a", href=True):
        text = a.get_text().strip()
        href = a["href"].strip()
        text_lower = text.lower()
        href_lower = href.lower()
        
        # Skip old archive years
        if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', text_lower):
            continue
            
        for kw, (exam_id, display_name) in targets.items():
            if kw in text_lower or kw in href_lower:
                if len(text) > 10:
                    full_url = href if href.startswith("http") else "https://nta.ac.in" + (href if href.startswith("/") else "/" + href)
                    if full_url not in [n["link"] for n in notices]:
                        notices.append({
                            "exam_id": exam_id,
                            "source_name": f"{display_name} - NTA",
                            "title": text,
                            "link": full_url,
                            "snippet": text
                        })
                        break
                        
        if len(notices) >= 3:
            break
            
    return notices
