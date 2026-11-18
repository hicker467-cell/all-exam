import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

STATE_PORTALS = [
    {
        "exam_id": "up_nmms",
        "source_name": "NMMS उत्तर प्रदेश (ENTDATA)",
        "url": "https://entdata.co.in",
        "keywords": ["nmms", "scholarship", "छात्रवृत्ति", "आवेदन", "प्रवेश पत्र", "परिणाम"]
    },
    {
        "exam_id": "mp_nmms",
        "source_name": "NMMS मध्य प्रदेश (RSK MP)",
        "url": "https://www.rskmp.in",
        "keywords": ["nmms", "मेधा", "कक्षा 8", "छात्रवृत्ति", "scholarship"]
    },
    {
        "exam_id": "rj_nmms",
        "source_name": "NMMS राजस्थान (शाला दर्पण)",
        "url": "https://rajshaladarpan.rajasthan.gov.in",
        "keywords": ["nmms", "scholarship", "मेधा", "छात्रवृत्ति"]
    },
    {
        "exam_id": "jh_nmms_akanksha",
        "source_name": "NMMS व आकांक्षा-40 (JAC झारखंड)",
        "url": "https://jac.jharkhand.gov.in",
        "keywords": ["nmms", "akanksha", "आकांक्षा", "छात्रवृत्ति", "मेधा", "scholarship"]
    },
    {
        "exam_id": "cg_nmms",
        "source_name": "NMMS छत्तीसगढ़ (SCERT)",
        "url": "https://scert.cg.gov.in",
        "keywords": ["nmms", "scholarship", "छात्रवृत्ति"]
    }
]

def scrape_nmms_multistate() -> list:
    """
    Scrapes NMMS scholarships across UP, MP, Rajasthan, Jharkhand and CG.
    Strictly filters out old archive years (2024-25, 2023-24, etc.).
    """
    notices = []
    
    for portal in STATE_PORTALS:
        html = fetch_html(portal["url"], timeout=12)
        if not html:
            continue
            
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            text = a.get_text().strip()
            href = a["href"].strip()
            text_lower = text.lower()
            href_lower = href.lower()
            
            # Skip old years
            if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', text_lower):
                continue
                
            if any(k in text_lower or k in href_lower for k in portal["keywords"]):
                if len(text) > 10:
                    full_url = href if href.startswith("http") else portal["url"].rstrip("/") + "/" + href.lstrip("/")
                    notices.append({
                        "exam_id": portal["exam_id"],
                        "source_name": portal["source_name"],
                        "title": text,
                        "link": full_url,
                        "snippet": text
                    })
                    break # Take top active notice per state portal
                    
    return notices
