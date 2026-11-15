from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.navodaya.gov.in/nvs/en/Home1/"

def scrape_navodaya() -> list:
    """
    Uses Playwright to render Navodaya's React SPA and extracts active admission notices.
    """
    notices = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = context.new_page()
            page.goto(URL, wait_until="load", timeout=25000)
            page.wait_for_timeout(2000)
            
            html = page.content()
            browser.close()
            
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all("a", href=True):
                text = link.get_text().strip()
                href = link["href"].strip()
                
                keywords = ["jnvst", "class vi", "class ix", "class xi", "admission", "selection test", "नवोदय", "प्रवेश"]
                if any(k in text.lower() or k in href.lower() for k in keywords):
                    if len(text) > 10:
                        full_url = href if href.startswith("http") else "https://www.navodaya.gov.in" + (href if href.startswith("/") else "/" + href)
                        notices.append({
                            "exam_id": "navodaya_jnvst",
                            "source_name": "नवोदय विद्यालय समिति (NVS)",
                            "title": text,
                            "link": full_url,
                            "snippet": text
                        })
    except Exception as e:
        print(f"Navodaya scraping error: {e}")
        
    return notices
