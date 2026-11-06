import os
from playwright.sync_api import sync_playwright

def test_milestone_1():
    print("==========================================")
    print("   Milestone 1: Environment Sanity Check  ")
    print("==========================================")

    # 1. Create screenshots directory
    os.makedirs("screenshots", exist_ok=True)

    print("\n[Playwright] Launching Chromium browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        target_url = "https://phptravels.com/demo"
        print(f"[Browser] Navigating to target site: {target_url}")
        page.goto(target_url, timeout=30000)

        page_title = page.title()
        print(f"[Success] Page loaded! Title: '{page_title}'")

        # Capture a verification screenshot
        screenshot_path = "screenshots/milestone1_sanity.png"
        page.screenshot(path=screenshot_path)
        print(f"[Proof] Screenshot captured at: {screenshot_path}")

        print("\n==========================================")
        print("  MILESTONE 1 VERIFIED: ENVIRONMENT READY!")
        print("==========================================")

        # Keeps browser open so you can inspect it visually
        input("\n--> Browser is open showing PHPTravels. Press ENTER in this terminal to close it...")
        browser.close()

if __name__ == "__main__":
    test_milestone_1()
