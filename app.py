import streamlit as st
import yaml
import random

# --- CONFIG ---
st.set_page_config(page_title="LexIQ Labs - Prompt Blender", layout="centered")
st.markdown("<h1 style='text-align:center;'>🧠 LexIQ Labs | AI-Personalized Prompt Blender</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- AUTH CHECK ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- PASSWORD FORM ---
if not st.session_state["authenticated"]:
    st.markdown("### 🔐 Secure Access")
    with st.form("login_form"):
        password = st.text_input("Enter Access Code", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if password == "DEMO2025":
                st.session_state["authenticated"] = True
                st.success("✅ Access granted. Scroll down to begin.")
            else:
                st.error("❌ Invalid access code.")
    st.stop()

# --- CATEGORY SELECTION ---
st.markdown("### 🎯 Select Your Use Case")
category = st.selectbox("Choose a role-specific prompt set:", ["Sales", "Support", "Success"])
category_key = category.lower()

# --- LOAD PROMPTS ---
try:
    with open("prompts.yaml", "r") as f:
        prompt_data = yaml.safe_load(f)
        fragments = prompt_data[category_key]
except Exception as e:
    st.error(f"⚠️ Error loading prompts: {e}")
    st.stop()

# --- FORM ---
st.markdown("### ✍️ Personalize Your Prompts")
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        prospect_name = st.text_input("Prospect Name", "Jordan")
        pain_point = st.text_input("Pain Point", "Slow onboarding")
        desired_outcome = st.text_input("Desired Outcome", "Faster conversion")
        wait_period = st.text_input("Wait Period", "2 weeks")
        goal_date = st.text_input("Goal Date", "August 15")
    with col2:
        future_timeline = st.text_input("Future Timeline", "60 days")
        competitor_name = st.text_input("Competitor Name", "Acme Corp")
        added_revenue = st.text_input("Added Revenue", "$10,000")
        impact_percent = st.text_input("Impact Percent", "30%")
        team_name = st.text_input("Team Name", "Growth Team")

    module_x = st.text_input("Module/Feature X", "Automation Suite")
    solution_x = st.text_input("Solution/Strategy X", "One-click Deploy")

    generate = st.form_submit_button("🔮 Blend Prompts")

# --- GENERATE PROMPTS ---
if generate:
    selected = random.sample(fragments, 5)
    st.success("✅ Prompts successfully generated!")

    for i, frag in enumerate(selected, 1):
        try:
            blended = frag.format(
                prospect_name=prospect_name,
                pain_point=pain_point,
                desired_outcome=desired_outcome,
                wait_period=wait_period,
                goal_date=goal_date,
                future_timeline=future_timeline,
                competitor_name=competitor_name,
                added_revenue=added_revenue,
                impact_percent=impact_percent,
                module_x=module_x,
                solution_x=solution_x,
                strategy_name="Retention Loop",
                team_name=team_name,
                feature_x="Analytics Dashboard",
                feature_y="Smart Alerts",
                feature_z="Lead Tracker",
                number_of_clients="25",
                framework_name="Value Hook",
                positioning_strategy="pain-solution framing",
                tactic_x="generic outreach",
                sales_channel="email outreach",
                new_wait_period="48 hours",
                next_quarter="Q4"
            )
        except KeyError as e:
            st.error(f"⚠️ Missing input for: {e}")
            continue

        chatgpt_prompt = (
            f"Write a persuasive email or message for a {category} persona.\n"
            f"Start with this hook: \"{blended}\"\n"
            f"Then expand with context, resolve {pain_point}, and include a clear CTA before closing."
        )

        st.markdown(f"---\n### 🔹 Prompt {i}")
        st.markdown(f"**🧠 Blended Line:**\n> {blended}")
        st.markdown("**💬 ChatGPT Expansion Prompt:**")
        st.code(chatgpt_prompt, language="markdown")
