import os
from playwright.sync_api import sync_playwright

os.makedirs("screenshots", exist_ok=True)

def test_navodaya_playwright():
    print("Testing Playwright Headless on Navodaya...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        page.goto("https://www.navodaya.gov.in/nvs/en/Home1/", wait_until="networkidle", timeout=30000)
        
        # Take screenshot of the rendered page
        screenshot_path = "screenshots/navodaya_test.png"
        page.screenshot(path=screenshot_path)
        print(f"Rendered Title: {page.title()}")
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Look for pop-up or notification links
        content = page.content()
        print(f"Rendered HTML Size: {len(content)} bytes")
        
        browser.close()

if __name__ == "__main__":
    test_navodaya_playwright()
