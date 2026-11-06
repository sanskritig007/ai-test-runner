# Autonomous AI Plain-English Test Runner

An intelligent test automation tool that takes test cases written in **plain English** (e.g., *"Log in as a customer and verify the dashboard is shown"*), autonomously navigates a browser using **Playwright**, interacts with page elements, and reports whether the test **PASSED** or **FAILED**.

Built for general-purpose web testing and tested against the [PHPTRAVELS Demo Platform](https://phptravels.com/demo).

---

## 🚀 Key Features

* **Natural Language Test Translation:** Accepts freeform English instructions without requiring predefined Gherkin syntax or rigid scripts.
* **Compact DOM Perception Engine (`browser_controller.py`):** Automatically filters thousands of lines of raw HTML noise, extracting only visible, human-interactable buttons, inputs, and links into a structured format.
* **Hybrid AI Planner (`ai_planner.py`):**
  * **Real LLM Integration:** Powered by Google Gemini (`gemini-1.5-flash`) via `GEMINI_API_KEY`.
  * **Zero-Friction Fallback:** Built-in Smart Intent Heuristics allow evaluators to run and review the tool immediately without configuring paid API keys.
* **General-Purpose & Non-Hardcoded:** Designed to run across different websites and novel test cases dynamically.
* **Audit Trail & Evidence:** Generates visual screenshot evidence (`screenshots/final_test_result.png`) and structured execution reports.

---

## 🛠️ Setup & Installation

### Prerequisites
* Python 3.9+ installed
* Internet connection

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/sanskritig007/ai-test-runner.git
cd ai-test-runner

python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies & Browser
```bash
pip install -r requirements.txt
playwright install chromium
```

*(Optional: If you wish to use live Google Gemini API, set your key: `export GEMINI_API_KEY="your-key-here"`. The tool will automatically use Gemini, or seamlessly fall back to the built-in Smart Intent Planner).*

---

## 🏃 Usage & Execution

### 1. Run Default PHPTRAVELS Test Case
```bash
python run_test.py
```
*This opens Chromium, analyzes the PHPTRAVELS demo site, performs customer login, verifies the dashboard, and outputs a colored test report.*

### 2. Run with Custom Website & Prompt
You can pass any URL and plain-English test case via command-line arguments:
```bash
python run_test.py --url "https://phptravels.com/demo" --prompt "Log in as a customer and verify the dashboard is shown"
```

### 3. Headless Mode (for CI/CD pipelines)
```bash
python run_test.py --headless
```

---

## 📋 Approach & Limitations Note

### Technical Approach
1. **ReAct Loop (Reasoning + Acting):** Rather than blindly generating an entire 20-step script upfront (which often fails on dynamic websites), the agent operates in an iterative loop:
   * **Observe:** Reads the active DOM's interactive elements and bounding boxes.
   * **Think:** The AI brain determines the single best next action.
   * **Act:** Executes the click or fill action via Playwright with auto-wait and scroll-into-view resilience.
   * **Verify:** Evaluates page state and URL changes to determine if the target condition is met.
2. **Selector Generation:** Prioritizes accessible labels, text anchors, and semantic attributes over fragile absolute XPaths.

### Honest Limitations & Engineering Trade-offs
* **Non-Deterministic Multi-Pathing:** On complex multi-portal websites with multiple buttons having similar labels (e.g. "Admin Login" vs "Customer Login" vs "Supplier Login"), an LLM without domain context may take an extra step to find the intended portal.
* **CAPTCHA & Bot Detection:** Cloudflare Turnstile, hCaptcha, and strict anti-bot protections intentionally block headless/automated browsers; autonomous agents require human intervention or bypass tokens on protected environments.
* **Rate Limits & Latency:** Real-time LLM inference introduces a 500ms–1500ms latency per step. For fast regression suites in production CI/CD, caching common intent paths is recommended.

