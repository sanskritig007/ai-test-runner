from browser_controller import BrowserController

def test_perception():
    print("==================================================")
    print("   Milestone 2: Page Perception Verification      ")
    print("==================================================")

    controller = BrowserController(headless=False)
    
    try:
        print("\n[Browser] Starting browser...")
        controller.start()

        target_url = "https://phptravels.com/demo"
        print(f"[Browser] Navigating to: {target_url}")
        controller.navigate(target_url)

        print("\n[Perception] Scanning page for interactive elements...")
        elements = controller.get_interactive_elements()
        print(f"[Success] Found {len(elements)} interactive elements on the page!")

        print("\n--- First 5 Elements Detected by the AI Eyes ---")
        for el in elements[:5]:
            print(f"  • Tag: <{el['tag']}> | Text: '{el['text']}' | Selector: {el['selector']}")
        print("-------------------------------------------------")

        screenshot = controller.take_screenshot("milestone2_perception")
        print(f"\n[Proof] Screenshot captured: {screenshot}")

        print("\n==================================================")
        print("   MILESTONE 2 VERIFIED: PERCEPTION ENGINE READY! ")
        print("==================================================")

        input("\n--> Press ENTER in this terminal to close the browser...")

    finally:
        controller.close()

if __name__ == "__main__":
    test_perception()

