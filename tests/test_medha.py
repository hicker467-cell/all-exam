import requests
import urllib3
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
for u in ["https://medhasoft.bihar.gov.in", "https://medhasoft.bihar.gov.in/medhamat2024/", "https://medhasoft.bihar.gov.in/medhainter2024/"]:
    try:
        r = requests.get(u, headers=headers, timeout=8, verify=False)
        print(f"[{r.status_code}] {u}: {len(r.content)} bytes")
    except Exception as e:
        print(f"[FAIL] {u}: {e}")
