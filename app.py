import streamlit as st
import gspread
import json
import os
import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Survival Automation",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS (Dark Theme, Green Accents, White Inputs) ----------
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    h1, h2, h3 {
        color: #00ff88 !important;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 8px;
        border: 1px solid #2a2f3a;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
    }
    .stButton > button {
        background-color: #00ff88 !important;
        color: #0e1117 !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #00cc6a !important;
        transform: scale(1.02);
    }
    .stAlert {
        background-color: #1e222b !important;
        color: #e0e0e0 !important;
    }
    /* Divider */
    hr {
        border-color: #2a2f3a;
    }
    /* Card-like sections */
    .bot-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #00ff88;
    }
    .price-tag {
        color: #00ff88;
        font-size: 1.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HERO SECTION ----------
st.title("⚡ Survival Automation")
st.markdown("### Stop burning time – let the bots handle it.")
st.write("We build **custom automation bots** that save you 10+ hours per week. Pick your weapon below.")

st.divider()

# ---------- BOTS / SERVICES SECTION ----------
st.subheader("🤖 Our Automation Bots")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="bot-card">
        <h4 style="color:#00ff88;">🔍 SEO Automation</h4>
        <p>Auto‑generate keyword clusters, track rankings, and produce content briefs – all on autopilot.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bot-card">
        <h4 style="color:#00ff88;">📞 Voice Agent</h4>
        <p>AI‑powered voice assistant that handles inbound calls, books appointments, and qualifies leads 24/7.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="bot-card">
        <h4 style="color:#00ff88;">📊 Data Scraper</h4>
        <p>Extract structured data from any website – competitors, pricing, reviews – delivered to your sheet.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bot-card">
        <h4 style="color:#00ff88;">✉️ Email Outreach</h4>
        <p>Personalized cold‑email sequences that follow up automatically and book meetings on your calendar.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------- PRICING SECTION ----------
st.subheader("💎 Investment Plans")

price_cols = st.columns(3)
prices = [
    ("Starter", "$1.5K", "1 bot, 3 months support"),
    ("Pro", "$4K", "2 bots, 6 months support + training"),
    ("Enterprise", "$7K", "Unlimited bots, 12 months support + dedicated onboarding")
]

for col, (tier, price, desc) in zip(price_cols, prices):
    with col:
        st.markdown(f"""
        <div style="background:#161b22; border-radius:12px; padding:1.5rem; text-align:center; border:1px solid #2a2f3a;">
            <h4 style="color:#e0e0e0;">{tier}</h4>
            <div class="price-tag">{price}</div>
            <p style="color:#a0a0a0; font-size:0.9rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ---------- LEAD FORM (with EMAIL added) ----------
st.subheader("📩 Ready to start? Drop your details.")

with st.form(key="lead_form", clear_on_submit=True):
    # ---- FIELDS ----
    name = st.text_input("Full Name *", placeholder="e.g. John Carter")
    email = st.text_input("Email Address *", placeholder="john@company.com")   # <-- NEW FIELD
    budget = st.selectbox(
        "Budget Range",
        options=["$1.5K", "$4K", "$7K"],
        index=0
    )
    message = st.text_area(
        "What problem do you want to solve?",
        placeholder="Tell us about your workflow, bottlenecks, or goals..."
    )

    # ---- SUBMIT BUTTON ----
    submitted = st.form_submit_button("🚀 Send Lead")

    if submitted:
        # Basic validation
        if not name.strip():
            st.error("Please enter your name.")
        elif not email.strip() or "@" not in email:
            st.error("Please enter a valid email address (e.g., name@domain.com).")
        else:
            # ---------- GOOGLE SHEETS INTEGRATION ----------
            try:
                # 1. Load credentials from Render secret file
                creds_path = "/etc/secrets/sheets_credentials.json"
                if not os.path.exists(creds_path):
                    st.error("🔐 Credentials file not found. Please add 'sheets_credentials.json' as a Secret File in Render.")
                else:
                    with open(creds_path, "r") as f:
                        creds_dict = json.load(f)

                    # 2. Authorize gspread
                    gc = gspread.service_account_from_dict(creds_dict)

                    # 3. Open the sheet by ID (from your report)
                    sheet_id = "1HgVeJsSivhZEAQpITk9SRbXEvqtdiWf65P_btPfHnf0"
                    sh = gc.open_by_key(sheet_id)
                    worksheet = sh.sheet1

                    # 4. Prepare row (ORDER: Name, Email, Budget, Message, Timestamp)
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    row_data = [name.strip(), email.strip(), budget, message.strip(), timestamp]

                    # 5. Append
                    worksheet.append_row(row_data)

                    # 6. Success (no balloons, no confetti – just a clean message)
                    st.success(f"🔥 {name}! We've saved your details. We'll reach out to {email} within 24 hours. ✅ Your message was saved to Google Sheets.")

            except gspread.exceptions.SpreadsheetNotFound:
                st.error("❌ Google Sheet not found. Check the Sheet ID and make sure the service account has Editor access.")
            except Exception as e:
                st.error(f"⚠️ Something went wrong: {str(e)}")

st.caption("💡 By submitting, you agree to our privacy policy. We hate spam as much as you do.")

# ---------- FOOTER ----------
st.divider()
st.markdown(
    "<p style='text-align:center; color:#666; font-size:0.8rem;'>© 2026 Survival Automation — Built with Streamlit & deployed on Render</p>",
    unsafe_allow_html=True
)