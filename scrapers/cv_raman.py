import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://state.bihar.gov.in/dst/CitizenHome.html"
BASE_DOMAIN = "https://state.bihar.gov.in"

def scrape_cv_raman() -> list:
    """
    Scrapes Sir CV Raman Science Talent Search / BCST Bihar notices
    from Department of Science, Technology and Technical Education, Bihar.
    Strictly filters out old archive years.
    """
    html = fetch_html(URL, timeout=20)
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    notices = []
    
    # Check notice tables, lists and marquee
    for link in soup.find_all("a", href=True):
        text = link.get_text().strip()
        href = link["href"].strip()
        text_lower = text.lower()
        
        # Skip old years
        if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', text_lower):
            continue
            
        # Check relevance to Science Talent / CV Raman / Ramanujan / BCST
        keywords = ["raman", "talent", "विज्ञान प्रतिभा", "रमन", "रामानुजन", "bcst", "olympiad"]
        if any(k in text_lower or k in href.lower() for k in keywords):
            full_url = href if href.startswith("http") else BASE_DOMAIN + (href if href.startswith("/") else "/" + href)
            notices.append({
                "exam_id": "bihar_cv_raman",
                "source_name": "BCST / विज्ञान विभाग, बिहार",
                "title": text or "Sir CV Raman Talent Search Notice",
                "link": full_url,
                "snippet": text
            })
            
    return notices
