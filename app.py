# app.py - Survival Automation Landing Page
# Uses gspread for Google Sheets (no Apps Script)

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime
from audit import quick_audit

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Survival Automation - Python + Spite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a Bug': None, 'About': None}
)

# --- GSC VERIFICATION (META TAG) ---
st.markdown(
    '<meta name="google-site-verification" content="8T7T-TcZtbw7cQjNeDV232admv4DD_PdwuCd812wE8s" />',
    unsafe_allow_html=True
)

# --- HIDE STREAMLIT TOOLBAR ---
st.markdown("""
<style>
div[data-testid="stToolbar"] { display: none !important; }
footer { visibility: hidden !important; }
header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNCTION: SAVE TO GOOGLE SHEETS USING GSPREAD ---
def save_to_google_sheets(name, email, budget, message):
    try:
        # 1. Load credentials from Render secret file
        creds_path = "/etc/secrets/sheets_credentials.json"
        if not os.path.exists(creds_path):
            return False, "Credentials file not found. Please add 'sheets_credentials.json' as a Secret File in Render."

        with open(creds_path, "r") as f:
            creds_dict = json.load(f)

        # 2. Authorize using service account
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)

        # 3. Open the sheet by ID
        sheet_id = "1HgVeJsSivhZEAQpITk9SRbXEvqtdiWf65P_btPfHnf0"
        sh = client.open_by_key(sheet_id)
        worksheet = sh.sheet1

        # 4. Prepare row: Name, Email, Budget, Message, Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [name, email, budget, message, timestamp]

        # 5. Append
        worksheet.append_row(row_data)
        return True, None

    except gspread.exceptions.SpreadsheetNotFound:
        return False, "Spreadsheet not found – check the sheet ID and permissions."
    except Exception as e:
        return False, str(e)

# --- CUSTOM CSS (with white background + black text fixes) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    * { font-family: 'JetBrains Mono', monospace; }
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    .main { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
    .hero-title { font-size: 3.5rem; font-weight: 700; color: #00FF88; line-height: 1.1; text-shadow: 0 0 40px rgba(0, 255, 136, 0.15); }
    .hero-sub { font-size: 1.2rem; color: #888; margin-top: 1rem; border-left: 3px solid #00FF88; padding-left: 1rem; }
    .badge { display: inline-block; background: rgba(0, 255, 136, 0.1); color: #00FF88; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(0, 255, 136, 0.2); margin: 0.2rem; }
    .sos-banner { background: #0a1a0f; border: 1px solid #00FF88; border-radius: 8px; padding: 0.8rem 1.5rem; text-align: center; margin: 0.5rem 0 1rem 0; font-size: 0.9rem; color: #00FF88; }
    .sos-banner .highlight { font-weight: 700; color: #00FF88; }
    .bot-card { background: #111; border: 1px solid #222; border-radius: 12px; padding: 1.5rem; height: 100%; transition: all 0.3s ease; }
    .bot-card:hover { border-color: #00FF88; transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0, 255, 136, 0.05); }
    .bot-card h3 { color: #00FF88; margin-bottom: 0.5rem; }
    .bot-card .cost { color: #00FF88; font-weight: 700; font-size: 1.2rem; }
    .bot-card .stack { color: #666; font-size: 0.8rem; background: #1a1a1a; padding: 0.3rem 0.6rem; border-radius: 4px; display: inline-block; margin: 0.2rem 0; }
    .pricing-card { background: #111; border: 1px solid #222; border-radius: 12px; padding: 2rem; text-align: center; height: 100%; transition: all 0.3s ease; }
    .pricing-card:hover { border-color: #00FF88; }
    .pricing-card .price { font-size: 2.5rem; font-weight: 700; color: #00FF88; }
    .pricing-card .feature { color: #aaa; padding: 0.3rem 0; border-bottom: 1px solid #1a1a1a; }
    .pricing-card .feature:last-child { border-bottom: none; }
    .pricing-card.popular { border-color: #00FF88; background: #0f1f15; }
    
    /* --- CONTACT FORM FIXES: white background + black text --- */
    .contact-form { background: #111; border-radius: 12px; padding: 2rem; border: 1px solid #222; }
    
    .contact-form input, .contact-form textarea {
        background: #ffffff !important;          /* white background */
        color: #000000 !important;               /* black text */
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        width: 100% !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .contact-form input::placeholder, .contact-form textarea::placeholder {
        color: #666666 !important;               /* gray placeholder */
        opacity: 1 !important;
    }
    .contact-form input:focus, .contact-form textarea:focus {
        border-color: #00FF88 !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
    }
    .contact-form label { color: #ddd !important; font-size: 0.9rem !important; }
    
    /* ---- Force textarea (message field) to be white with black text ---- */
    .stTextArea textarea {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stTextArea textarea::placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    
    /* Submit button: white background + black text for maximum contrast */
    .stButton button {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: 2px solid #cccccc !important;
        padding: 0.6rem 2rem !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
        border-color: #00FF88 !important;
    }
    
    .section-title { font-size: 2.5rem; font-weight: 700; color: #00FF88; text-align: center; margin-bottom: 2rem; }
    .section-sub { text-align: center; color: #888; margin-bottom: 3rem; }
    .stat-number { font-size: 3rem; font-weight: 700; color: #00FF88; text-align: center; }
    .stat-label { color: #666; text-align: center; font-size: 0.9rem; }
    .footer { text-align: center; color: #444; font-size: 0.8rem; border-top: 1px solid #1a1a1a; padding-top: 2rem; margin-top: 3rem; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 1rem; background: #111; border-radius: 12px; padding: 0.5rem; }
    .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; padding: 0.5rem 1.5rem; color: #666; font-family: 'JetBrains Mono', monospace; }
    .stTabs [aria-selected="true"] { background: rgba(0, 255, 136, 0.1); color: #00FF88; }
    @media (max-width: 768px) { .hero-title { font-size: 2rem; } .section-title { font-size: 1.8rem; } .stat-number { font-size: 2rem; } }
</style>
""", unsafe_allow_html=True)

# --- SOS BANNER ---
st.markdown("""
<div class="sos-banner">
    💪 <span class="highlight">Built on a borrowed laptop</span> — if it runs on this, it runs anywhere.
</div>
""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.markdown('<div class="main">', unsafe_allow_html=True)

# --- HERO ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="margin-top: 1rem;">
        <span class="badge">⚡ Python + Spite</span>
        <span class="badge">$0 Infra</span>
        <span class="badge">Built on Borrowed Laptop</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="hero-title">I replace your $500/mo Zapier stack with one Python system you own. $0 to run.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="hero-sub">
        Zero-cost builds with Python + Spite on a borrowed laptop. 10 bots, $0 infra.<br>
        <span style="color: #555; font-size: 0.9rem;">Francis · Automation Engineer · CDO, PH</span>
    </p>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("⚡ See Live Bots", use_container_width=True):
            pass
    with col_b:
        if st.button("💰 Book Build - $4-7K", use_container_width=True):
            pass

with col2:
    st.markdown("""
    <div style="background: #111; border: 1px solid #00FF88; border-radius: 12px; padding: 1.5rem; text-align: center; margin-top: 1rem;">
        <div style="font-size: 3rem;">🔥</div>
        <div style="color: #00FF88; font-weight: 700; font-size: 1.2rem;">Survival Mode</div>
        <div style="color: #666; font-size: 0.8rem;">Zero-cost builds · Python · Spite</div>
        <div style="color: #444; font-size: 0.7rem; margin-top: 0.5rem;">Borrowed laptop. Still shipping.</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- PROBLEM vs MY WAY ---
st.markdown('<h2 class="section-title">💀 No-Code vs Survival</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: #1a0a0a; border: 1px solid #441111; border-radius: 12px; padding: 2rem;">
        <h3 style="color: #ff4444; margin-top: 0;">❌ No-Code Way</h3>
        <ul style="color: #888; list-style: none; padding-left: 0;">
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #1a1a1a;">💰 $30/mo per tool</li>
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #1a1a1a;">💔 Breaks at 2am</li>
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #1a1a1a;">😤 You wait for support</li>
            <li style="padding: 0.5rem 0;">🔒 You don't own the logic</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #0a1a0f; border: 1px solid #00FF88; border-radius: 12px; padding: 2rem;">
        <h3 style="color: #00FF88; margin-top: 0;">✅ Survival Way</h3>
        <ul style="color: #aaa; list-style: none; padding-left: 0;">
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #1a1a1a;">💰 $0 to run</li>
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #1a1a1a;">💪 I own the logic</li>
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #1a1a1a;">🔧 Fix at 2:03am</li>
            <li style="padding: 0.5rem 0;">🚀 You own the code</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- LIVE BOTS ---
st.markdown('<h2 class="section-title" id="bots">🤖 Live Bots</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">All built with Python + Spite. $0 to run. You own them.</p>', unsafe_allow_html=True)

# --- TABS: only SEO Automation and Free SEO Audit ---
tab1, tab2 = st.tabs(["📈 SEO Automation", "🔍 Free SEO Audit"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="bot-card">
            <h3>📈 SEO Automation System</h3>
            <p style="color: #aaa;">Turns GSC data into a ready-to-use content strategy in 15 minutes. Scores keywords, rejects bad ones, learns from mistakes.</p>
            <div>
                <span class="stack">Python</span>
                <span class="stack">GSC API</span>
                <span class="stack">Groq (Free)</span>
                <span class="stack">Streamlit</span>
            </div>
            <p class="cost">Cost to run: $0</p>
            <p style="color: #666; font-size: 0.8rem;">Any niche. Any industry. 15 minutes.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: #111; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid #222; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 4rem;">📈</div>
            <div style="color: #00FF88; font-weight: 700;">GSC → Content</div>
            <div style="color: #666; font-size: 0.8rem;">15 minutes. Any niche.</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("💰 Want this bot? $4-7K build", key="seo_bot_btn"):
        st.success("🔥 Let's build it! Contact me below.")

with tab2:
    # ----- SEO AUDIT TAB with EMAIL field -----
    st.markdown("### 🚀 Free Instant SEO Audit")
    st.write("Enter your website URL and email to get a quick SEO health check + actionable fixes.")

    url_input = st.text_input("Website URL", placeholder="https://example.com")
    email_audit = st.text_input("Your Email *", placeholder="you@example.com")

    if st.button("Run Audit", key="audit_btn"):
        if url_input and email_audit:
            with st.spinner("Auditing... this may take a few seconds."):
                # Run the audit
                result = quick_audit(url_input)
                
                # --- SAVE TO GOOGLE SHEETS ---
                # Column 1: URL (so you see the domain)
                # Column 2: Email
                # Column 3: Budget (blank)
                # Column 4: Message (SEO Audit)
                # Column 5: Timestamp
                save_success, save_error = save_to_google_sheets(
                    name=url_input,      # <-- URL goes in Column 1
                    email=email_audit,
                    budget="",
                    message="SEO Audit"
                )
                if not save_success:
                    st.warning(f"Email was captured but could not save to sheet: {save_error}")
                else:
                    st.success("✅ Email saved to Google Sheets.")
                
                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Page Title", result["title"])
                    st.metric("Speed Score", f"{result['speed_score']}/100")
                    st.metric("H1 Count", result["h1_count"])
                with col2:
                    st.metric("Word Count", result["word_count"])
                    st.metric("Meta Description", "✅ Present" if result["has_meta"] else "❌ Missing")
                    st.metric("External Links (sellable spots)", result["link_spots"])

                st.markdown("### 🔧 Top 3 Fixes")
                st.success(f"1️⃣ {result['fix_1']}")
                st.info(f"2️⃣ {result['fix_2']}")
                st.warning(f"3️⃣ {result['fix_3']}")

                st.markdown("---")
                st.markdown(f"**Thanks {email_audit}!** Your email has been captured. Want these fixed automatically? That's exactly what my **SEO Automation Bot** does. [Contact me](#contact) to build one for you.")
        elif not url_input:
            st.error("Please enter a valid URL.")
        else:
            st.error("Please enter your email address.")

st.divider()

# --- HOW IT WORKS ---
st.markdown('<h2 class="section-title">⚡ How It Works</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">📝</div>
        <h3 style="color: #00FF88;">1. Describe</h3>
        <p style="color: #888;">You describe your broken workflow. I listen and understand.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">⚙️</div>
        <h3 style="color: #00FF88;">2. Build</h3>
        <p style="color: #888;">I rebuild it in Python in 48 hours. You see progress daily.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">🚀</div>
        <h3 style="color: #00FF88;">3. Own</h3>
        <p style="color: #888;">You own the code. $0 monthly. Deploy anywhere.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- PRICING ---
st.markdown('<h2 class="section-title">💰 Pricing</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">One build. You own it. No monthly retainer.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="pricing-card">
        <h3 style="color: #aaa;">Starter</h3>
        <div class="price">$1.5K</div>
        <div style="color: #666; font-size: 0.9rem;">Fix 1 broken workflow</div>
        <div style="margin-top: 1rem;">
            <div class="feature">✅ Replace 1 Zap/Make</div>
            <div class="feature">✅ Python rewrite</div>
            <div class="feature">✅ You own the code</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pricing-card popular">
        <div style="color: #00FF88; font-size: 0.8rem; font-weight: 700;">🔥 MOST POPULAR</div>
        <h3 style="color: #00FF88;">Standard</h3>
        <div class="price">$4K</div>
        <div style="color: #666; font-size: 0.9rem;">1 custom bot</div>
        <div style="margin-top: 1rem;">
            <div class="feature">✅ SEO Automation System</div>
            <div class="feature">✅ Full Python codebase</div>
            <div class="feature">✅ $0 to run forever</div>
            <div class="feature">✅ 48h delivery</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="pricing-card">
        <h3 style="color: #aaa;">Premium</h3>
        <div class="price">$7K</div>
        <div style="color: #666; font-size: 0.9rem;">3 bot system</div>
        <div style="margin-top: 1rem;">
            <div class="feature">✅ 3 custom bots</div>
            <div class="feature">✅ Unified dashboard</div>
            <div class="feature">✅ Unlimited users</div>
            <div class="feature">✅ Priority support</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- PROOF ---
st.markdown('<h2 class="section-title">📊 Proof</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-number">120+</div>
    <div class="stat-label">Workflows Replaced</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-number">25K</div>
    <div class="stat-label">Tasks Automated</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-number">300+</div>
    <div class="stat-label">Hours Saved</div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-number">$0</div>
    <div class="stat-label">Monthly Infra Cost</div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #555; font-size: 0.9rem; margin-top: 1rem;">
    Tech: Python · Groq Free · Edge-TTS · Telegram · Sheets · Supabase · Streamlit
</div>
""", unsafe_allow_html=True)

st.divider()

# --- CONTACT FORM ---
st.markdown('<h2 class="section-title" id="contact">📩 Let\'s Build</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Describe your pain. I\'ll rebuild it in Python. $4-7K. You own it.</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    
    with st.form("contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Your Name", placeholder="Juan Dela Cruz")
            email = st.text_input("📧 Your Email", placeholder="juan@example.com")
            budget = st.selectbox("💰 Budget Range", ["$1.5K - Starter", "$4K - Standard", "$7K - Premium", "Flexible"])
        with col2:
            message = st.text_area("😤 What workflow is broken?", placeholder="I'm spending $500/mo on 5 tools that break...", height=100)
        
        submitted = st.form_submit_button("⚡ Send - Let's Build It")
        
        if submitted:
            if name and email and message:
                success, error = save_to_google_sheets(name, email, budget, message)
                if success:
                    st.success(f"🔥 {name}! Let's fix your workflow. I'll reach out to {email} within 24 hours.")
                    st.info("✅ Your message was saved to Google Sheets.")
                else:
                    st.error(f"❌ Failed to save to Google Sheets: {error}")
                    st.info("📝 Your message was received, but the sheet wasn't updated. I'll manually check.")
                    st.json({"name": name, "email": email, "message": message, "budget": budget})
            else:
                st.error("⚠️ Please fill in Name, Email, and Message fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🐍 Built on Python + Spite</div>
    <div style="color: #555;">Francis · Automation Engineer · Cagayan de Oro, PH</div>
    <div style="color: #333; font-size: 0.7rem; margin-top: 0.5rem;">
        Borrowed laptop. Zero budget. Still shipping. 💪
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)