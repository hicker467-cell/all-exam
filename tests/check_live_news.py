import requests
from bs4 import BeautifulSoup
from config import BROWSER_HEADERS
import urllib3
urllib3.disable_warnings()

r = requests.get("https://www.livehindustan.com/career/", headers=BROWSER_HEADERS, verify=False, timeout=12)
soup = BeautifulSoup(r.text, "html.parser")

articles = []
for a in soup.find_all("a", href=True):
    title = a.get_text().strip()
    href = a["href"].strip()
    if len(title) > 30 and "/career/" in href:
        full_url = href if href.startswith("http") else "https://www.livehindustan.com" + href
        if full_url not in [x["url"] for x in articles]:
            articles.append({"title": title, "url": full_url})
            if len(articles) >= 6:
                break

for i, art in enumerate(articles, 1):
    print(f"{i}. {art['title']}")
    print(f"   Link: {art['url']}\n")
