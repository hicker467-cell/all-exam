import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

STATE_PORTALS = [
    {
        "exam_id": "up_nmms",
        "source_name": "NMMS उत्तर प्रदेश (ENTDATA)",
        "url": "https://entdata.co.in",
        "keywords": ["राष्ट्रीय आय एवं योग्यता", "nmms exam", "nmmss", "कक्षा 8 छात्रवृत्ति"]
    },
    {
        "exam_id": "mp_nmms",
        "source_name": "NMMS मध्य प्रदेश (RSK MP)",
        "url": "https://www.rskmp.in",
        "keywords": ["राष्ट्रीय मीन्स कम मेरिट", "nmms 202", "nmms परीक्षा"]
    },
    {
        "exam_id": "rj_nmms",
        "source_name": "NMMS राजस्थान (शाला दर्पण)",
        "url": "https://rajshaladarpan.rajasthan.gov.in",
        "keywords": ["nmms परीक्षा", "nmmss", "राष्ट्रीय साधन सह मेधा"]
    },
    {
        "exam_id": "jh_nmms_akanksha",
        "source_name": "NMMS व आकांक्षा-40 (JAC झारखंड)",
        "url": "https://jac.jharkhand.gov.in",
        "keywords": ["nmms exam", "nmmss", "akanksha 40", "आकांक्षा-40", "आकांक्षा 40", "राष्ट्रीय साधन सह मेधा"]
    },
    {
        "exam_id": "cg_nmms",
        "source_name": "NMMS छत्तीसगढ़ (SCERT)",
        "url": "https://scert.cg.gov.in",
        "keywords": ["nmms परीक्षा", "nmmss", "राष्ट्रीय साधन सह मेधा छात्रवृत्ति"]
    }
]

GENERIC_NAV_WORDS = [
    "scholarship portal", "portal", "home", "login", "contact", "about us",
    "dashboard", "registration portal", "student login", "school login"
]

def scrape_nmms_multistate() -> list:
    """
    Scrapes NMMS scholarships across UP, MP, Rajasthan, Jharkhand and CG.
    Strictly filters out old archive years (2024-25, 2023-24, etc.) and generic menu buttons.
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
            
            # Skip generic navbar / menu items
            if any(text_lower == g for g in GENERIC_NAV_WORDS):
                continue
                
            # Skip old years
            if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', text_lower):
                continue
                
            if any(k in text_lower or k in href_lower for k in portal["keywords"]):
                if len(text) > 12: # Avoid tiny button text
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
