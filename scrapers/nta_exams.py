import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

def scrape_nta_exams() -> list:
    """
    Scrapes National Testing Agency (NTA) dedicated portal (exams.nta.nic.in)
    specifically for:
    - All India Sainik Schools Entrance Exam (AISSEE)
    - SHRESHTA-NETS Scheme
    Only captures concrete public notices and active application form links.
    """
    notices = []
    
    # 1. Sainik School Dedicated Page
    url_sainik = "https://exams.nta.nic.in/sainik-school-society/"
    html_sainik = fetch_html(url_sainik, timeout=15)
    if html_sainik:
        soup = BeautifulSoup(html_sainik, "html.parser")
        for a in soup.find_all("a", href=True):
            text = a.get_text().strip()
            href = a["href"].strip()
            t_lower = text.lower()
            
            # Look for active application / public notices
            if any(k in t_lower for k in ["application form", "inviting online", "public notice", "admit card", "examination date"]):
                # Skip old years
                if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', t_lower):
                    continue
                if len(text) > 15:
                    full_url = href if href.startswith("http") else "https://exams.nta.nic.in" + (href if href.startswith("/") else "/" + href)
                    if full_url not in [n["link"] for n in notices]:
                        notices.append({
                            "exam_id": "national_sainik_school",
                            "source_name": "सैनिक स्कूल प्रवेश परीक्षा (AISSEE - NTA)",
                            "title": text,
                            "link": full_url,
                            "snippet": text
                        })
                        if len(notices) >= 2:
                            break

    # 2. SHRESHTA Dedicated Page
    url_shreshta = "https://exams.nta.nic.in/shreshta/"
    html_shreshta = fetch_html(url_shreshta, timeout=15)
    if html_shreshta:
        soup = BeautifulSoup(html_shreshta, "html.parser")
        for a in soup.find_all("a", href=True):
            text = a.get_text().strip()
            href = a["href"].strip()
            t_lower = text.lower()
            
            if any(k in t_lower for k in ["application", "public notice", "admit card", "score card"]):
                if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', t_lower):
                    continue
                if len(text) > 15:
                    full_url = href if href.startswith("http") else "https://exams.nta.nic.in" + (href if href.startswith("/") else "/" + href)
                    if full_url not in [n["link"] for n in notices]:
                        notices.append({
                            "exam_id": "nta_shreshta",
                            "source_name": "श्रेष्ठ योजना (SHRESHTA - NTA)",
                            "title": text,
                            "link": full_url,
                            "snippet": text
                        })
                        break
                        
    return notices
