import streamlit as st
import yaml
import random
from datetime import date

# ──────────────────────────────  CONFIG  ────────────────────────────── #
st.set_page_config(page_title="LexIQ Labs – Prompt Blender", layout="centered")

HEADER_HTML = """
<h1 style="text-align:center;margin-bottom:0.2em;">
  🧠 LexIQ Labs | Prompt Blender
</h1>
<p style="text-align:center;font-size:0.9rem;color:#888;">
  Turn sales objections &amp; customer hurdles into persuasive AI messages
</p><hr style="margin-top:0.2em;">
"""
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# ─────────────────────────────  LOGIN  ──────────────────────────────── #
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    with st.form("login_form"):
        st.markdown("### 🔐 Secure Access")
        pwd = st.text_input("Access code", type="password", placeholder="Enter your passcode")
        if st.form_submit_button("Login"):
            if pwd == "DEMO2025":                # ← change your code here
                st.session_state["authenticated"] = True
                st.success("Access granted – scroll down to begin.")
            else:
                st.error("Invalid code. Try again.")
    st.stop()

# ───────────────────────  CATEGORY & PROMPT LOAD  ───────────────────── #
st.markdown("### 🎯 Pick Your Scenario")
category = st.selectbox("Use‑case", ["Sales", "Support", "Success"])
cat_key   = category.lower()

try:
    with open("prompts.yaml", "r") as f:
        data = yaml.safe_load(f)
        fragments      = data[cat_key]                            # 60 blended lines
        gpt_templates  = data["gpt_prompt_templates"][cat_key]    # role‑specific templates
except Exception as err:
    st.error(f"Could not load prompts.yaml → {err}")
    st.stop()

# ──────────────────────────────  FORM  ──────────────────────────────── #
st.markdown("### ✍️  Enter Context")

with st.form("context"):
    col1, col2 = st.columns(2)
    with col1:
        pain_point      = st.text_input("Objection / Pain Point*",  placeholder="“It’s too expensive”")
        desired_outcome = st.text_input("Your Goal*",               placeholder="“Show ROI & close deal”")
        prospect_name   = st.text_input("Prospect Name (optional)", placeholder="Jordan")
    with col2:
        # advanced expander
        with st.expander("🔧 Advanced  (optional)"):
            goal_date        = st.text_input("Goal Date",           placeholder="30 July")
            future_timeline  = st.text_input("Future Timeline",     placeholder="60 days")
            added_revenue    = st.text_input("Added Revenue",       placeholder="$10 000")
            impact_percent   = st.text_input("Impact %",            placeholder="25 %")
            competitor_name  = st.text_input("Competitor Name",     placeholder="Acme Inc.")
            wait_period      = st.text_input("Wait Period",         placeholder="2 weeks")
            module_x         = st.text_input("Feature / Module X",  placeholder="Analytics Suite")
            solution_x       = st.text_input("Solution X",          placeholder="ROI Playbook")
            team_name        = st.text_input("Team Name",           placeholder="Growth Team")

    submitted = st.form_submit_button("🔮  Blend Prompts")

# ─────────────────────────────  GENERATE  ───────────────────────────── #
if submitted:
    st.success("Prompts generated – copy & paste into ChatGPT")
    st.markdown("---")

    # build dict of all possible vars to avoid KeyError
    ctx = {
        "pain_point": pain_point,
        "desired_outcome": desired_outcome,
        "prospect_name": prospect_name or "your prospect",
        "wait_period": wait_period,
        "goal_date": goal_date,
        "future_timeline": future_timeline,
        "competitor_name": competitor_name,
        "added_revenue": added_revenue,
        "impact_percent": impact_percent,
        "module_x": module_x,
        "solution_x": solution_x,
        "team_name": team_name,
        "strategy_name": "Retention Loop",
        "feature_x": "Analytics Dashboard",
        "feature_y": "Smart Alerts",
        "feature_z": "Lead Tracker",
        "number_of_clients": "25",
        "framework_name": "Value Hook",
        "positioning_strategy": "pain‑solution framing",
        "tactic_x": "generic outreach",
        "sales_channel": "email outreach",
        "new_wait_period": "48 hours",
        "next_quarter": "Q4",
        "today": date.today().strftime("%d %b %Y")
    }

    # choose 5 blended lines
    blended_lines  = random.sample(fragments, 5)
    for idx, line in enumerate(blended_lines, 1):
        try:
            blended = line.format(**ctx)
        except KeyError as miss:
            st.error(f"Missing variable in YAML: {miss}")
            continue

        # pick a role‑specific GPT template & inject
        gpt_template = random.choice(gpt_templates)
        chatgpt_prompt = gpt_template.format(blended_line=blended, **ctx)

        # ── UI BLOCK ──
        st.markdown(f"#### 🔹 Prompt {idx}")
        st.markdown(f"<div style='padding:6px;background:#222;border-radius:6px;color:#EEE;'><em>{blended}</em></div>", unsafe_allow_html=True)
        st.markdown("**💬 ChatGPT Instruction:**")
        st.code(chatgpt_prompt, language="markdown")
        st.markdown("<hr style='border:1px dashed #555;'>", unsafe_allow_html=True)
