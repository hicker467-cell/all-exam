import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Test Variants for failed URLs
url_tests = [
    # 1. BCST variants
    ("BCST HTTP", "http://bcst.org.in"),
    ("BCST Govt Portal", "https://state.bihar.gov.in/dst/"),
    # 2. Sainik School / NTA variants
    ("NTA Main Portal", "https://nta.ac.in"),
    ("NTA Notice Board", "https://nta.ac.in/NoticeBoardArchive"),
    ("AISSEE NTA Nic", "https://aissee.nta.nic.in"),
    ("AISSEE Exams NTA", "https://exams.nta.ac.in/"),
    # 3. Bihar BCEBCW (OBC Kanya Awasiya) variants
    ("BCEBCW Main", "https://state.bihar.gov.in/bcebc/"),
    ("BCEBCW Portal 2", "https://state.bihar.gov.in/bcebcw/"),
    ("Bihar Backward Welfare", "https://state.bihar.gov.in/bcebcw/CitizenHome.html"),
    # 4. BSEB Patna variants (increased timeout to 30s)
    ("BSEB HTTPS 30s", "https://biharboardonline.bihar.gov.in"),
    ("BSEB Secondary", "https://secondary.biharboardonline.com"),
    # 5. Navodaya (testing redirect follow)
    ("Navodaya Main", "https://www.navodaya.gov.in/nvs/en/Home1/"),
    ("Navodaya Admission Portal", "https://cbseitms.nic.in/2025/nvsentry11/")
]

for label, url in url_tests:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, verify=False, allow_redirects=True)
        print(f"[{r.status_code}] {label} -> Final URL: {r.url} ({len(r.content)} bytes)")
    except Exception as e:
        print(f"[FAIL] {label} -> {e}")
