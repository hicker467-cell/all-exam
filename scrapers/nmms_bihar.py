from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://scert.bihar.gov.in"

def scrape_nmms_bihar() -> list:
    """
    Scrapes NMMS (National Means-cum-Merit Scholarship) and NTSE notices from SCERT Bihar.
    """
    html = fetch_html(URL, timeout=20)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    notices = []
    
    for link in soup.find_all("a", href=True):
        text = link.get_text().strip()
        href = link["href"].strip()
        
        keywords = ["nmms", "nmmss", "means", "merit", "छात्रवृत्ति", "मेधा", "scholarship"]
        if any(k in text.lower() or k in href.lower() for k in keywords):
            full_url = href if href.startswith("http") else URL + (href if href.startswith("/") else "/" + href)
            notices.append({
                "exam_id": "bihar_nmms",
                "source_name": "SCERT बिहार",
                "title": text or "SCERT Bihar NMMS Notice",
                "link": full_url,
                "snippet": text
            })
            
    return notices
