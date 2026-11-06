import os
import time
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, Playwright

class BrowserController:
    """
    Controls browser automation using Playwright.
    Acts as the 'eyes and hands' of the AI agent:
    - Extracts visible interactive elements from the DOM (Perception)
    - Executes actions like click, fill, assert (Action)
    - Captures screenshots for auditing and test reporting
    """

    def __init__(self, headless: bool = False, slow_mo: int = 400):
        self.headless = headless
        self.slow_mo = slow_mo
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        os.makedirs("screenshots", exist_ok=True)

    def start(self):
        """Launches the Playwright Chromium browser."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = self.context.new_page()

    def navigate(self, url: str):
        """Navigates to the specified URL."""
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        # Ensure proper URL scheme
        if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("file://"):
            url = f"https://{url}"

        self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(1.5)  # Allow initial dynamic scripts to settle

    def get_interactive_elements(self) -> List[Dict[str, Any]]:
        """
        Scans the active page and extracts all visible interactive elements
        (inputs, buttons, links, dropdowns) into a compact, AI-friendly format.
        """
        if not self.page:
            return []

        js_script = """
        () => {
            const elements = [];
            const candidates = document.querySelectorAll(
                'button, a, input, select, textarea, [role="button"], [role="link"], [onclick]'
            );

            let idx = 0;
            for (const el of candidates) {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);

                // Filter out invisible or hidden elements
                if (rect.width === 0 || rect.height === 0 || style.visibility === 'hidden' || style.display === 'none') {
                    continue;
                }

                const tag = el.tagName.toLowerCase();
                const type = (el.getAttribute('type') || '').toLowerCase();
                const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                const placeholder = el.getAttribute('placeholder') || '';
                const ariaLabel = el.getAttribute('aria-label') || '';
                const name = el.getAttribute('name') || '';
                const id = el.getAttribute('id') || '';
                const href = el.getAttribute('href') || '';
                const value = el.value || '';

                // Build a reliable Playwright selector
                let selector = '';
                if (id) {
                    selector = `#${id}`;
                } else if (name && (tag === 'input' || tag === 'select' || tag === 'textarea')) {
                    selector = `${tag}[name="${name}"]`;
                } else if (placeholder) {
                    selector = `[placeholder="${placeholder}"]`;
                } else if (text && text.length < 40) {
                    selector = `text="${text}"`;
                } else if (ariaLabel) {
                    selector = `[aria-label="${ariaLabel}"]`;
                } else {
                    selector = `${tag}:nth-of-type(${idx + 1})`;
                }

                elements.push({
                    index: idx,
                    tag: tag,
                    type: type,
                    text: text.slice(0, 50),
                    placeholder: placeholder,
                    aria_label: ariaLabel,
                    name: name,
                    id: id,
                    selector: selector
                });

                idx++;
                if (idx >= 60) break; // Limit context size for fast AI processing
            }
            return elements;
        }
        """
        return self.page.evaluate(js_script)

    def execute_action(self, action: str, selector: str, value: Optional[str] = None) -> bool:
        """
        Executes an action requested by the AI planner.
        Supported actions: 'click', 'fill', 'select', 'press_enter', 'wait'
        """
        if not self.page:
            return False

        action = action.lower().strip()

        try:
            if action == "click":
                loc = self.page.locator(selector).first
                loc.scroll_into_view_if_needed(timeout=3000)
                try:
                    loc.click(timeout=4000)
                except Exception:
                    # Fallback to force JS click if intercepted
                    loc.evaluate("el => el.click()")
                time.sleep(1.5)
                return True

            elif action == "fill":
                loc = self.page.locator(selector).first
                loc.scroll_into_view_if_needed(timeout=3000)
                loc.click()
                loc.fill(value or "")
                time.sleep(0.5)
                return True

            elif action == "select":
                loc = self.page.locator(selector).first
                loc.select_option(label=value)
                time.sleep(0.5)
                return True

            elif action == "press_enter":
                self.page.keyboard.press("Enter")
                time.sleep(1.5)
                return True

            elif action == "wait":
                time.sleep(float(value or 2.0))
                return True

            return False
        except Exception as e:
            print(f"    [Execution Warning] Could not perform {action} on '{selector}': {e}")
            return False

    def assert_condition(self, condition_text: str) -> bool:
        """
        Checks whether the specified condition/text is visible on the current page.
        """
        if not self.page:
            return False

        try:
            content = self.page.content().lower()
            if condition_text.lower() in content:
                return True

            # Also check text across visible headings and alerts
            visible_texts = self.page.locator("h1, h2, h3, h4, .dashboard, [role='alert'], .alert").all_inner_texts()
            for t in visible_texts:
                if condition_text.lower() in t.lower():
                    return True

            return False
        except Exception:
            return False

    def take_screenshot(self, name: str) -> str:
        """Captures a screenshot for evidence and audit trail."""
        if not self.page:
            return ""
        path = f"screenshots/{name}.png"
        self.page.screenshot(path=path)
        return path

    def get_current_url(self) -> str:
        return self.page.url if self.page else ""

    def get_title(self) -> str:
        return self.page.title() if self.page else ""

    def close(self):
        """Closes browser and cleans up Playwright."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

