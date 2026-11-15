import requests
import urllib3
from config import BROWSER_HEADERS
urllib3.disable_warnings()

# Testing corrected domains
urls = [
    ("Rajasthan Shala Darpan Gov", "https://rajshaladarpan.rajasthan.gov.in"),
    ("Rajasthan Shala Darpan HTTP", "http://rajshaladarpan.nic.in"),
    ("Medhasoft HTTP", "http://medhasoft.bih.nic.in"),
]

for label, u in urls:
    try:
        r = requests.get(u, headers=BROWSER_HEADERS, timeout=12, verify=False, allow_redirects=True)
        print(f"[{r.status_code}] {label}: {len(r.content)} bytes received")
    except Exception as e:
        print(f"[FAIL] {label}: {e}")
