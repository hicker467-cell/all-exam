import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

def scrape_atal_awasiya() -> list:
    """
    Scrapes Atal Awasiya Vidyalaya admission circulars and notifications
    from both the dedicated admission portal (avs.upsdc.gov.in) and UPBOCW (upbocw.in).
    Admissions are for Class 6 and Class 9 for children of registered workers.
    """
    notices = []
    
    # 1. Dedicated Portal
    html_avs = fetch_html("https://avs.upsdc.gov.in", timeout=15)
    if html_avs:
        soup = BeautifulSoup(html_avs, "html.parser")
        for a in soup.find_all("a", href=True):
            text = a.get_text().strip()
            href = a["href"].strip()
            text_lower = text.lower()
            if any(k in text_lower for k in ["admission", "प्रवेश", "फॉर्म", "पंजीकरण", "notification", "विज्ञप्ति"]):
                if not re.search(r'\b(202[0-4]|2024[-_ ]?25)\b', text_lower):
                    full_url = href if href.startswith("http") else "https://avs.upsdc.gov.in/" + href.lstrip("/")
                    notices.append({
                        "exam_id": "up_atal_awasiya",
                        "source_name": "अटल आवासीय विद्यालय प्रवेश (AVS / UPBOCW)",
                        "title": text,
                        "link": full_url,
                        "snippet": text
                    })

    # 2. UPBOCW Official Circulars
    html_bocw = fetch_html("https://upbocw.in", timeout=15)
    if html_bocw:
        soup = BeautifulSoup(html_bocw, "html.parser")
        for a in soup.find_all("a", href=True):
            text = a.get_text().strip()
            href = a["href"].strip()
            text_lower = text.lower()
            if any(k in text_lower for k in ["atal", "अटल", "awasiya", "आवासीय"]) and any(k in text_lower for k in ["admission", "प्रवेश", "योजना", "विद्यालय"]):
                if not re.search(r'\b(202[0-4]|2024[-_ ]?25)\b', text_lower):
                    full_url = href if href.startswith("http") else "https://upbocw.in/" + href.lstrip("/")
                    if full_url not in [n["link"] for n in notices]:
                        notices.append({
                            "exam_id": "up_atal_awasiya",
                            "source_name": "अटल आवासीय विद्यालय प्रवेश (UPBOCW)",
                            "title": text,
                            "link": full_url,
                            "snippet": text
                        })
                        
    return notices
