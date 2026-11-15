import os
import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target Sites to test
TEST_TARGETS = [
    {"name": "Sir CV Raman / BCST Bihar", "url": "https://state.bihar.gov.in/dst/CitizenHome.html"},
    {"name": "BCST Official", "url": "https://bcst.org.in"},
    {"name": "NMMS Bihar (SCERT)", "url": "https://scert.bihar.gov.in"},
    {"name": "Navodaya Vidyalaya Samiti", "url": "https://navodaya.gov.in/nvs/en/Home1"},
    {"name": "Sainik School / NTA", "url": "https://exams.nta.ac.in/AISSEE"},
    {"name": "Bihar BCEBCW (OBC Kanya Awasiya)", "url": "https://state.bihar.gov.in/bcebcw/CitizenHome.html"},
    {"name": "BSEB Patna (Simultala/Boards)", "url": "https://biharboardonline.bihar.gov.in"},
    {"name": "BCECEB Bihar (Polytechnic/ITI)", "url": "https://bceceboard.bihar.gov.in"},
    {"name": "Live Hindustan Education", "url": "https://www.livehindustan.com/career/"},
    {"name": "Prabhat Khabar Education", "url": "https://www.prabhatkhabar.com/education"}
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

def test_fetch(item):
    name = item["name"]
    url = item["url"]
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12, verify=False)
        print(f"[{resp.status_code}] {name}: {len(resp.content)} bytes received")
        return {"name": name, "status": resp.status_code, "ok": resp.status_code == 200, "size": len(resp.content)}
    except Exception as e:
        print(f"[FAIL] {name} ({url}): {e}")
        return {"name": name, "status": "ERROR", "ok": False, "error": str(e)}

if __name__ == "__main__":
    print("Testing Website Accessibility...")
    results = []
    for target in TEST_TARGETS:
        results.append(test_fetch(target))
