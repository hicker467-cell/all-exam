import requests
import urllib3
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

r = requests.get('https://www.navodaya.gov.in/nvs/en/Home1/', headers=headers, verify=False, timeout=10)
print("Status:", r.status_code)
print("Content:\n", r.text[:500])
