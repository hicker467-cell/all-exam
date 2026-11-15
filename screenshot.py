import os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_screenshot(url: str, filename_prefix: str) -> str:
    """
    Spins up headless Chromium, renders the target notice URL with SSL bypass and realistic headers.
    Returns the absolute path of the saved PNG screenshot, or None if failed.
    """
    clean_prefix = "".join(c for c in filename_prefix if c.isalnum() or c == "_")[:30]
    out_path = os.path.join(SCREENSHOT_DIR, f"{clean_prefix}.png")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--ignore-certificate-errors", "--disable-gpu", "--no-sandbox"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                ignore_https_errors=True # Crucial for Govt sites with invalid/expired SSL
            )
            page = context.new_page()
            
            # Fast load - abort heavy third-party media / ads
            page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["media", "font"] else route.continue_())
            
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(1000)
            
            page.screenshot(path=out_path)
            browser.close()
            return out_path
    except Exception as e:
        print(f"Screenshot Error on {url}: {e}")
        return None
