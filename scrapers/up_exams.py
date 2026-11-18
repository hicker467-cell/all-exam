import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

def scrape_up_exams() -> list:
    """
    Scrapes key Uttar Pradesh portals:
    - UPMSP (UP Board 10th & 12th)
    - JEECUP (UP Polytechnic Entrance)
    - VidyaGyan School (Class 6 Rural Talent)
    Strictly filters out old archive years (2024-25, 2023-24, etc.).
    """
    notices = []
    
    # 1. UPMSP
    html_upmsp = fetch_html("https://upmsp.edu.in", timeout=12)
    if html_upmsp:
        soup = BeautifulSoup(html_upmsp, "html.parser")
        for a in soup.find_all("a", href=True):
            t = a.get_text().strip()
            h = a["href"].strip()
            t_lower = t.lower()
            if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', t_lower):
                continue
            if any(k in t_lower or k in h.lower() for k in ["समय सारणी", "admit", "विज्ञप्ति", "हाईस्कूल", "इण्टरमीडिएट"]):
                if len(t) > 15:
                    full_url = h if h.startswith("http") else "https://upmsp.edu.in/" + h.lstrip("/")
                    notices.append({
                        "exam_id": "upmsp_board",
                        "source_name": "UP Board (UPMSP प्रयागराज)",
                        "title": t,
                        "link": full_url,
                        "snippet": t
                    })
                    break
                    
    # 2. JEECUP
    html_jeecup = fetch_html("https://jeecup.admissions.nic.in", timeout=12)
    if html_jeecup:
        soup = BeautifulSoup(html_jeecup, "html.parser")
        for a in soup.find_all("a", href=True):
            t = a.get_text().strip()
            h = a["href"].strip()
            t_lower = t.lower()
            if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', t_lower):
                continue
            if any(k in t_lower or k in h.lower() for k in ["upjee", "jeecup", "polytechnic", "admit card", "registration"]):
                if len(t) > 10:
                    full_url = h if h.startswith("http") else "https://jeecup.admissions.nic.in/" + h.lstrip("/")
                    notices.append({
                        "exam_id": "jeecup_polytechnic_up",
                        "source_name": "UP पॉलिटेक्निक (JEECUP)",
                        "title": t,
                        "link": full_url,
                        "snippet": t
                    })
                    break
                    
    # 3. VidyaGyan
    html_vg = fetch_html("https://vidyagyan.in", timeout=12)
    if html_vg:
        soup = BeautifulSoup(html_vg, "html.parser")
        for a in soup.find_all("a", href=True):
            t = a.get_text().strip()
            h = a["href"].strip()
            t_lower = t.lower()
            if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', t_lower):
                continue
            if any(k in t_lower or k in h.lower() for k in ["admission", "prelim", "entrance", "apply"]):
                if len(t) > 10:
                    full_url = h if h.startswith("http") else "https://vidyagyan.in/" + h.lstrip("/")
                    notices.append({
                        "exam_id": "vidyagyan_school_up",
                        "source_name": "विद्याज्ञान स्कूल (UP)",
                        "title": t,
                        "link": full_url,
                        "snippet": t
                    })
                    break
                    
    return notices
