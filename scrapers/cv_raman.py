from bs4 import BeautifulSoup
from scrapers.base import fetch_html

URL = "https://state.bihar.gov.in/dst/CitizenHome.html"
BASE_DOMAIN = "https://state.bihar.gov.in"

def scrape_cv_raman() -> list:
    """
    Scrapes Sir CV Raman Science Talent Search / BCST Bihar notices
    from Department of Science, Technology and Technical Education, Bihar.
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
        
        # Check relevance to Science Talent / CV Raman / Ramanujan / BCST
        keywords = ["raman", "science", "bcst", "talent", "vigyan", "रमन", "प्रतिभा", "छात्रवृत्ति", "olympiad"]
        if any(k in text.lower() or k in href.lower() for k in keywords):
            full_url = href if href.startswith("http") else BASE_DOMAIN + (href if href.startswith("/") else "/" + href)
            notices.append({
                "exam_id": "bihar_cv_raman",
                "source_name": "BCST / विज्ञान विभाग, बिहार",
                "title": text or "Sir CV Raman Talent Search Notice",
                "link": full_url,
                "snippet": text
            })
            
    # Also grab the latest 3 general notices if specific keywords not found in title
    if not notices:
        for link in soup.find_all("a", href=True)[:5]:
            text = link.get_text().strip()
            href = link["href"].strip()
            if len(text) > 20 and (href.endswith(".pdf") or "CitizenHome" in href or "notice" in href.lower()):
                full_url = href if href.startswith("http") else BASE_DOMAIN + (href if href.startswith("/") else "/" + href)
                notices.append({
                    "exam_id": "bihar_cv_raman",
                    "source_name": "BCST / विज्ञान विभाग, बिहार",
                    "title": text,
                    "link": full_url,
                    "snippet": text
                })
                break
                
    return notices
