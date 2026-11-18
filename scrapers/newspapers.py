import re
from bs4 import BeautifulSoup
from scrapers.base import fetch_html

# Exact target keywords for Sagar Coaching Centre (School & Scholarship Exams)
TARGET_KEYWORDS = [
    "nmms", "nmmss", "रमन टैलेंट", "रामानुजन", "नवोदय", "jnvst", "सैनिक स्कूल", "aissee",
    "सिमुलतला", "sav प्रवेश", "मैट्रिक परीक्षा", "इंटर परीक्षा", "मेधा छात्रवृत्ति",
    "अटल आवासीय", "पॉलिटेक्निक प्रवेश", "iti प्रवेश", "मेधासॉफ्ट", "कन्या उत्थान",
    "विद्याज्ञान", "बोर्ड परीक्षा टाइम टेबल", "बोर्ड एडमिट कार्ड"
]

# Blacklist of irrelevant news (civil services, adult jobs, police, clickbait, legal)
BLACKLIST_WORDS = [
    "upsc", "bpsc", "civil judge", "कांस्टेबल", "police", "दरोगा", "ड्राइवर",
    "interview schedule", "इंटरव्यू", "कहानी", "सफलता की कहानी", "प्रेरणादायक",
    "aibe", "bar council", "ugc net", "neet pg", "banking", "ibps", "रेलवे ग्रुप डी"
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
    Scrapes strictly filtered, breaking school exam and scholarship announcements
    from Live Hindustan and Prabhat Khabar Education.
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
                        
    return notices
