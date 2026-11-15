import requests
import urllib3
from config import BROWSER_HEADERS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_html(url: str, timeout: int = 15) -> str:
    """
    Polite HTTP fetcher with browser-like headers, automatic redirect handling,
    and SSL error suppression for government certificates.
    """
    try:
        resp = requests.get(
            url,
            headers=BROWSER_HEADERS,
            timeout=timeout,
            verify=False,
            allow_redirects=True
        )
        if resp.status_code == 200:
            return resp.text
        print(f"HTTP {resp.status_code} on {url}")
        return ""
    except Exception as e:
        print(f"Fetch failed on {url}: {e}")
        return ""
