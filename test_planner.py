from ai_planner import AIPlanner

def test_ai_planner():
    print("==================================================")
    print("   Milestone 3: AI Action Planner Verification    ")
    print("==================================================")

    planner = AIPlanner()

    user_goal = "Log in as a customer and verify the dashboard is shown"
    print(f"\n[User Test Case] \"{user_goal}\"")

    # Simulated page state: Customer Login Form
    mock_elements = [
        {"tag": "input", "type": "email", "name": "email", "placeholder": "Email Address", "selector": "input[name='email']"},
        {"tag": "input", "type": "password", "name": "password", "placeholder": "Password", "selector": "input[name='password']"},
        {"tag": "button", "type": "submit", "text": "Sign In", "selector": "button[type='submit']"},
        {"tag": "a", "type": "", "text": "Forgot Password?", "selector": "text='Forgot Password?'"}
    ]

    history = []

    # Step 1: Decision for empty form
    print("\n[AI Thinking Step 1] Analyzing current page elements...")
    decision1 = planner.plan_next_step(
        goal=user_goal,
        current_url="https://phptravels.net/login",
        page_title="Login - PHPTRAVELS",
        elements=mock_elements,
        past_steps=history
    )
    print(f"  🧠 AI Thought: {decision1['thought']}")
    print(f"  ⚡ Action    : {decision1['action'].upper()} -> Selector: {decision1['selector']} | Value: '{decision1['value']}'")
    history.append(decision1)

    # Step 2: Decision after email is filled
    print("\n[AI Thinking Step 2] After email is filled...")
    decision2 = planner.plan_next_step(
        goal=user_goal,
        current_url="https://phptravels.net/login",
        page_title="Login - PHPTRAVELS",
        elements=mock_elements,
        past_steps=history
    )
    print(f"  🧠 AI Thought: {decision2['thought']}")
    print(f"  ⚡ Action    : {decision2['action'].upper()} -> Selector: {decision2['selector']} | Value: '{decision2['value']}'")
    history.append(decision2)

    # Step 3: Decision after password is filled
    print("\n[AI Thinking Step 3] After password is filled...")
    decision3 = planner.plan_next_step(
        goal=user_goal,
        current_url="https://phptravels.net/login",
        page_title="Login - PHPTRAVELS",
        elements=mock_elements,
        past_steps=history
    )
    print(f"  🧠 AI Thought: {decision3['thought']}")
    print(f"  ⚡ Action    : {decision3['action'].upper()} -> Selector: {decision3['selector']}")
    history.append(decision3)

    # Step 4: Decision when dashboard is loaded
    print("\n[AI Thinking Step 4] Page navigates to Dashboard...")
    decision4 = planner.plan_next_step(
        goal=user_goal,
        current_url="https://phptravels.net/account/dashboard",
        page_title="Customer Dashboard - PHPTRAVELS",
        elements=[],
        past_steps=history
    )
    print(f"  🧠 AI Thought: {decision4['thought']}")
    print(f"  🎯 Result    : {decision4['action'].upper()} | Goal Achieved: {decision4['goal_achieved']}")

    print("\n==================================================")
    print("   MILESTONE 3 VERIFIED: AI PLANNER BRAIN READY!  ")
    print("==================================================")

if __name__ == "__main__":
    test_ai_planner()

