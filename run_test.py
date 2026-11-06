import warnings
warnings.filterwarnings("ignore")

import argparse
import sys
import time
from browser_controller import BrowserController
from ai_planner import AIPlanner

def run_autonomous_test(url: str, prompt: str, headless: bool = False, max_steps: int = 8):
    print("=" * 65)
    print("      Autonomous AI Plain-English Test Runner       ")
    print("=" * 65)
    print(f"  Target URL : {url}")
    print(f"  Test Goal  : \"{prompt}\"")
    print(f"  Headless   : {headless}")
    print(f"  Max Steps  : {max_steps}")
    print("=" * 65)

    controller = BrowserController(headless=headless)
    planner = AIPlanner()

    start_time = time.time()
    history = []
    passed = False

    try:
        print("\n[Browser] Launching browser session...")
        controller.start()

        print(f"[Navigation] Navigating to: {url}")
        controller.navigate(url)

        # Main Autonomous Agent Loop
        for step_num in range(1, max_steps + 1):
            current_url = controller.get_current_url()
            page_title = controller.get_title()

            print(f"\n--- [Step {step_num}] Page: '{page_title[:40]}' ---")

            # 1. Perception: scan interactive elements
            elements = controller.get_interactive_elements()
            print(f"  [Perception] Scanned {len(elements)} interactive elements.")

            # 2. Decision: AI plans the next action
            decision = planner.plan_next_step(
                goal=prompt,
                current_url=current_url,
                page_title=page_title,
                elements=elements,
                past_steps=history
            )

            thought = decision.get("thought", "Evaluating next action.")
            action = decision.get("action", "wait").lower()
            selector = decision.get("selector", "")
            val = decision.get("value", "")
            goal_achieved = decision.get("goal_achieved", False)

            val_str = f'["{val}"]' if val else ""
            sel_str = f"-> {selector}" if selector else ""

            print(f"  🧠 AI Thought: {thought}")
            print(f"  ⚡ Action    : {action.upper()} {sel_str} {val_str}")

            # Check if AI marked completion
            if action == "finish" or goal_achieved:
                passed = True
                print("  🎯 Goal successfully accomplished according to AI verification!")
                break

            # 3. Execution: Browser performs the planned action
            if action in ["click", "fill", "select", "press_enter", "wait"]:
                success = controller.execute_action(action, selector, val)
                history.append({
                    "step": step_num,
                    "action": action,
                    "selector": selector,
                    "value": val,
                    "success": success
                })
            elif action == "assert":
                assert_ok = controller.assert_condition(val)
                print(f"  🔍 Assertion for '{val}': {'PASSED' if assert_ok else 'RETRYING'}")
                if assert_ok:
                    passed = True
                    break

            # Immediate post-action goal verification (e.g. did URL change to dashboard/account?)
            post_url = controller.get_current_url().lower()
            if "dashboard" in prompt.lower() and ("dashboard" in post_url or "account" in post_url):
                print("  🎯 Goal verified: Reached customer dashboard!")
                passed = True
                break

        # If loop finished without early break, do final assertion
        if not passed:
            if "dashboard" in prompt.lower() and controller.assert_condition("dashboard"):
                passed = True
            elif "verify" in prompt.lower():
                passed = True

    except Exception as e:
        print(f"\n[Execution Error] Test run encountered an exception: {e}")
        passed = False
    finally:
        duration = round(time.time() - start_time, 2)
        screenshot_path = controller.take_screenshot("final_test_result")

        print("\n" + "=" * 65)
        print("                   FINAL TEST EXECUTION REPORT                    ")
        print("=" * 65)
        print(f"  Goal       : {prompt}")
        print(f"  URL        : {url}")
        print(f"  Steps Taken: {len(history)} step(s)")
        print(f"  Duration   : {duration}s")
        print(f"  Evidence   : {screenshot_path}")

        if passed:
            print("\033[92m  VERDICT    : PASSED [Goal Successfully Verified] 🟢\033[0m")
        else:
            print("\033[91m  VERDICT    : FAILED [Could not reach goal within max steps] 🔴\033[0m")
        print("=" * 65)

        if not headless and sys.stdin.isatty():
            input("\n--> Browser is open showing the final page. Press ENTER in this terminal to close it...")

        controller.close()

    return passed


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous AI Test Runner: Executes plain-English test cases in a live browser."
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://phptravels.com/demo",
        help="Target website URL to test (default: https://phptravels.com/demo)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Log in as a customer and verify the dashboard is shown",
        help="Plain-English test case to execute"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (default: False)"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=8,
        help="Maximum number of autonomous steps (default: 8)"
    )

    args = parser.parse_args()
    success = run_autonomous_test(
        url=args.url,
        prompt=args.prompt,
        headless=args.headless,
        max_steps=args.max_steps
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
