import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

# Target keywords for Sagar Coaching Centre (School & Scholarship Entrance Exams in Hindi & English)
TARGET_KEYWORDS = [
    "nmms", "nmmss", "रमन टैलेंट", "रामानुजन", "ramanujan", "cv raman", "नवोदय", "jnvst", "navodaya",
    "सैनिक स्कूल", "aissee", "sainik school", "सिमुलतला", "sav admission", "simultala",
    "मैट्रिक परीक्षा", "इंटर परीक्षा", "मेधा छात्रवृत्ति", "अटल आवासीय", "atal awasiya",
    "पॉलिटेक्निक", "polytechnic", "jeecup", "dcece", "iticat", "iti admission",
    "मेधासॉफ्ट", "कन्या उत्थान", "विद्याज्ञान", "vidyagyan", "बोर्ड परीक्षा", "board exam",
    "hall ticket", "admit card", "एडमिट कार्ड", "प्रवेश पत्र"
]

# Blacklist of irrelevant news (civil services, adult jobs, police, clickbait, legal)
BLACKLIST_WORDS = [
    "upsc", "bpsc", "civil judge", "कांस्टेबल", "police", "दरोगा", "ड्राइवर", "driver",
    "interview schedule", "इंटरव्यू", "कहानी", "सफलता की कहानी", "प्रेरणादायक",
    "aibe", "bar council", "ugc net", "neet pg", "banking", "ibps", "रेलवे ग्रुप डी",
    "perfectionism", "zomato", "cyclone", "internship", "philippines"
]

def is_relevant_article(title: str) -> bool:
    t_lower = title.lower()
    
    # 1. Reject blacklisted topics
    if any(b in t_lower for b in BLACKLIST_WORDS):
        return False
        
    # 2. Reject old year references
    if re.search(r'\b(202[0-4]|2024[-_ ]?25|2023[-_ ]?24)\b', t_lower):
        return False
        
    # 3. Must match at least one relevant exam keyword
    if not any(k in t_lower for k in TARGET_KEYWORDS):
        return False
        
    return True

def scrape_newspapers() -> list:
    """
    Scrapes strictly filtered, breaking and advance exam/scholarship announcements
    from Top Trusted Media:
    1. Live Hindustan Career (Hindi)
    2. Prabhat Khabar Education (Hindi)
    3. Times of India - TOI Education (English/National)
    4. The Indian Express - Education (English/National)
    """
    notices = []
    
    # 1. Live Hindustan Career
    html_hindustan = fetch_html("https://www.livehindustan.com/career/", timeout=15)
    if html_hindustan:
        soup = BeautifulSoup(html_hindustan, "html.parser")
        for a in soup.find_all("a", href=True):
            title = a.get_text().strip()
            href = a["href"].strip()
            if len(title) > 20 and is_relevant_article(title):
                full_url = href if href.startswith("http") else "https://www.livehindustan.com" + href
                if full_url not in [n["link"] for n in notices]:
                    notices.append({
                        "exam_id": "hindi_newspaper_alert",
                        "source_name": "लाइव हिन्दुस्तान (शिक्षा समाचार)",
                        "title": title,
                        "link": full_url,
                        "snippet": title
                    })
                    if len(notices) >= 2:
                        break
                        
    # 2. Prabhat Khabar Education
    html_prabhat = fetch_html("https://www.prabhatkhabar.com/education", timeout=15)
    if html_prabhat:
        soup = BeautifulSoup(html_prabhat, "html.parser")
        count = 0
        for a in soup.find_all("a", href=True):
            title = a.get_text().strip()
            href = a["href"].strip()
            if len(title) > 20 and is_relevant_article(title):
                full_url = href if href.startswith("http") else "https://www.prabhatkhabar.com" + href
                if full_url not in [n["link"] for n in notices]:
                    notices.append({
                        "exam_id": "hindi_newspaper_alert",
                        "source_name": "प्रभात खबर (शिक्षा समाचार)",
                        "title": title,
                        "link": full_url,
                        "snippet": title
                    })
                    count += 1
                    if count >= 2:
                        break

    # 3. Times of India (TOI Education RSS)
    xml_toi = fetch_html("https://timesofindia.indiatimes.com/rssfeeds/913168846.cms", timeout=12)
    if xml_toi:
        try:
            tree = ET.fromstring(xml_toi)
            count = 0
            for item in tree.findall(".//item"):
                t_elem = item.find("title")
                l_elem = item.find("link")
                if t_elem is not None and l_elem is not None:
                    title = (t_elem.text or "").strip()
                    link = (l_elem.text or "").strip()
                    if len(title) > 20 and is_relevant_article(title):
                        if link not in [n["link"] for n in notices]:
                            notices.append({
                                "exam_id": "hindi_newspaper_alert",
                                "source_name": "Times of India (TOI Education)",
                                "title": title,
                                "link": link,
                                "snippet": title
                            })
                            count += 1
                            if count >= 2:
                                break
        except Exception as e:
            print(f"Error parsing TOI RSS: {e}")

    # 4. The Indian Express (Education RSS)
    xml_ie = fetch_html("https://indianexpress.com/section/education/feed/", timeout=12)
    if xml_ie:
        try:
            tree = ET.fromstring(xml_ie)
            count = 0
            for item in tree.findall(".//item"):
                t_elem = item.find("title")
                l_elem = item.find("link")
                if t_elem is not None and l_elem is not None:
                    title = (t_elem.text or "").strip()
                    link = (l_elem.text or "").strip()
                    if len(title) > 20 and is_relevant_article(title):
                        if link not in [n["link"] for n in notices]:
                            notices.append({
                                "exam_id": "hindi_newspaper_alert",
                                "source_name": "The Indian Express (Education)",
                                "title": title,
                                "link": link,
                                "snippet": title
                            })
                            count += 1
                            if count >= 2:
                                break
        except Exception as e:
            print(f"Error parsing Indian Express RSS: {e}")
            
    return notices
