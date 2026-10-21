
import streamlit as st
import textwrap

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Nexa AI | Intelligent Customer Support",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# HTML RENDERING HELPER
# ==========================================

def render_html(content):
    st.html(textwrap.dedent(content).strip())


# ==========================================
# CUSTOM CSS AND ANIMATIONS
# ==========================================

render_html("""
<style>

html {
    scroll-behavior: smooth;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background: #080d19;
    color: #ffffff;
}

/* Main container */

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* Animated background */

.stApp::before {
    content: "";
    position: fixed;
    width: 650px;
    height: 650px;
    top: -200px;
    left: -200px;
    background: radial-gradient(
        circle,
        rgba(110, 80, 230, 0.28),
        transparent 70%
    );
    filter: blur(40px);
    animation: backgroundMove 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 650px;
    height: 650px;
    bottom: -250px;
    right: -200px;
    background: radial-gradient(
        circle,
        rgba(30, 140, 190, 0.20),
        transparent 70%
    );
    filter: blur(40px);
    animation: backgroundMove 10s ease-in-out infinite alternate-reverse;
    pointer-events: none;
    z-index: 0;
}

@keyframes backgroundMove {
    from {
        transform: translate(0, 0) scale(0.9);
    }

    to {
        transform: translate(100px, 70px) scale(1.2);
    }
}

/* Navigation */

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    position: relative;
    z-index: 2;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 2px;
}

.brand span {
    color: #a995ff;
}

.nav-links {
    color: #c1c9dc;
    font-size: 13px;
    letter-spacing: 1.5px;
}

/* Hero */

.hero {
    text-align: center;
    padding: 100px 15px 35px;
    position: relative;
    z-index: 1;
    animation: fadeUp 1.2s ease both;
}

.eyebrow {
    display: inline-block;
    color: #c4b6ff;
    background: rgba(143,116,255,0.12);
    border: 1px solid rgba(170,145,255,0.35);
    border-radius: 40px;
    padding: 12px 20px;
    font-size: 11px;
    letter-spacing: 2px;
}

.hero h1 {
    font-size: clamp(42px, 7vw, 80px);
    line-height: 1.15;
    font-weight: 850;
    letter-spacing: -3px;
    color: white;
    margin-top: 30px;
    margin-bottom: 20px;
}

.gradient-text {
    background: linear-gradient(
        90deg,
        #a996ff,
        #75c9ff,
        #c1a5ff,
        #a996ff
    );
    background-size: 250% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientFlow 5s linear infinite;
}

@keyframes gradientFlow {
    to {
        background-position: 250% center;
    }
}

.hero-description {
    max-width: 720px;
    margin: auto;
    color: #aebbd0;
    font-size: 17px;
    line-height: 1.9;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(35px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Start button */

.stButton {
    position: relative;
    z-index: 2;
}

.stButton > button {
    min-height: 55px;
    border-radius: 13px;
    border: 1px solid #a995ff;
    background: linear-gradient(
        100deg,
        #6951c9,
        #9272eb
    );
    color: white;
    font-weight: 700;
    font-size: 15px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(
        100deg,
        #8169e7,
        #a38bff
    );
    color: white;
    border-color: white;
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(125,100,255,0.25);
}

/* Dashboard preview */

.preview {
    position: relative;
    z-index: 1;
    max-width: 1050px;
    margin: 65px auto 35px;
    padding: 30px;
    border: 1px solid rgba(170,150,255,0.3);
    border-radius: 22px;
    background: linear-gradient(
        145deg,
        rgba(34,44,68,0.96),
        rgba(15,23,42,0.96)
    );
    box-shadow: 0 25px 90px rgba(0,0,0,0.45);
    animation: floatCard 6s ease-in-out infinite;
    overflow: hidden;
}

.preview::before {
    content: "";
    position: absolute;
    width: 400px;
    height: 400px;
    top: -200px;
    left: -100px;
    background: rgba(130,110,255,0.15);
    filter: blur(70px);
    pointer-events: none;
}

.preview-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
    position: relative;
}

.preview-title {
    color: white;
    font-size: 21px;
    font-weight: 750;
}

.status {
    color: #7ce5b1;
    font-size: 12px;
    letter-spacing: 1px;
}

.preview-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    position: relative;
}

.preview-item {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 23px;
    transition: all 0.35s ease;
}

.preview-item:hover {
    transform: translateY(-7px);
    background: rgba(130,110,255,0.12);
    border-color: #a995ff;
}

.preview-icon {
    font-size: 34px;
    margin-bottom: 12px;
}

.preview-item h3 {
    color: white;
    font-size: 17px;
    margin: 5px 0;
}

.preview-item p {
    color: #aab8cf;
    font-size: 12px;
    margin-bottom: 0;
}

@keyframes floatCard {
    0%, 100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-12px);
    }
}

/* Animated sound wave */

.wave-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-top: 25px;
    position: relative;
}

.wave {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 60px;
}

.wave span {
    width: 5px;
    height: 14px;
    background: #a995ff;
    border-radius: 10px;
    animation: waveMove 1s ease-in-out infinite alternate;
}

.wave span:nth-child(2n) {
    animation-delay: .2s;
}

.wave span:nth-child(3n) {
    animation-delay: .4s;
}

.wave span:nth-child(4n) {
    animation-delay: .6s;
}

@keyframes waveMove {
    from {
        height: 12px;
    }

    to {
        height: 48px;
    }
}

.wave-label {
    color: #b8c4da;
    font-size: 13px;
}

/* Features */

.section-heading {
    text-align: center;
    margin-top: 100px;
    margin-bottom: 35px;
    position: relative;
    z-index: 1;
}

.section-heading .small-title {
    color: #a995ff;
    font-size: 12px;
    letter-spacing: 2px;
}

.section-heading h2 {
    font-size: 36px;
    color: white;
    margin-top: 12px;
}

.feature-card {
    position: relative;
    z-index: 1;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 26px;
    min-height: 180px;
    transition: all 0.35s ease;
}

.feature-card:hover {
    transform: translateY(-9px);
    border-color: #a995ff;
    background: rgba(130,105,255,0.12);
    box-shadow: 0 15px 35px rgba(85,70,170,0.2);
}

.feature-icon {
    font-size: 34px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: white;
    font-size: 19px;
}

.feature-card p {
    color: #aab5c9;
    font-size: 13px;
    line-height: 1.8;
}

/* Footer */

.footer {
    position: relative;
    z-index: 1;
    border-top: 1px solid rgba(255,255,255,0.12);
    padding: 35px 5px;
    text-align: center;
    color: #8995ac;
    font-size: 12px;
    margin-top: 90px;
}

/* Mobile responsive */

@media(max-width:700px) {
    .preview-grid {
        grid-template-columns: 1fr;
    }

    .nav-links {
        display: none;
    }

    .hero {
        padding-top: 60px;
    }

    .hero h1 {
        letter-spacing: -1px;
    }

    .preview {
        padding: 18px;
    }

    .section-heading h2 {
        font-size: 27px;
    }

    .wave-label {
        font-size: 10px;
    }
}

</style>
""")


# ==========================================
# NAVIGATION BAR
# ==========================================

render_html("""
<div class="navbar">
    <div class="brand">
        ✦ NEXA<span> AI</span>
    </div>

    <div class="nav-links">
        PRODUCTS &nbsp;&nbsp;&nbsp;
        SOLUTIONS &nbsp;&nbsp;&nbsp;
        SUPPORT
    </div>
</div>
""")


# ==========================================
# HERO SECTION
# ==========================================

render_html("""
<div class="hero">

    <div class="eyebrow">
        ✦ NEXT GENERATION AI CUSTOMER EXPERIENCE
    </div>

    <h1>
        The Future of Customer<br>
        <span class="gradient-text">
            Support is Here.
        </span>
    </h1>

    <p class="hero-description">
        Experience intelligent customer service powered by AI.
        Connect through text, voice and phone calls —
        all from one unified support platform.
    </p>

</div>
""")


# ==========================================
# START CHAT BUTTON
# ==========================================

left, center, right = st.columns([1, 1.4, 1])

with center:

    if st.button(
        "✦ START CHATTING  →",
        use_container_width=True
    ):
        st.switch_page("pages/1_Chat.py")


render_html("""
<div style="
    text-align:center;
    color:#8995ad;
    font-size:12px;
    margin-top:12px;">
    Experience intelligent customer support
</div>
""")


# ==========================================
# DASHBOARD PREVIEW
# ==========================================

render_html("""
<div class="preview">

    <div class="preview-header">

        <div class="preview-title">
            ✦ Nexa AI Support Center
        </div>

        <div class="status">
            ● PLATFORM PREVIEW
        </div>

    </div>

    <div class="preview-grid">

        <div class="preview-item">
            <div class="preview-icon">💬</div>
            <h3>Text Support</h3>
            <p>Customer conversations</p>
        </div>

        <div class="preview-item">
            <div class="preview-icon">🎙️</div>
            <h3>Voice Support</h3>
            <p>Natural voice interaction</p>
        </div>

        <div class="preview-item">
            <div class="preview-icon">☎️</div>
            <h3>Phone Support</h3>
            <p>Automated phone calls</p>
        </div>

    </div>

    <div class="wave-container">

        <div class="wave-label">
            Intelligent conversations
        </div>

        <div class="wave">
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
            <span></span><span></span>
        </div>

        <div class="wave-label">
            Connected support
        </div>

    </div>

</div>
""")


# ==========================================
# FEATURES SECTION
# ==========================================

render_html("""
<div class="section-heading">

    <div class="small-title">
        ONE PLATFORM. MULTIPLE CHANNELS.
    </div>

    <h2>
        Support Without Limits.
    </h2>

</div>
""")


col1, col2, col3 = st.columns(3)

with col1:

    render_html("""
    <div class="feature-card">

        <div class="feature-icon">💬</div>

        <h3>AI Text Chat</h3>

        <p>
            Answer customer questions, understand issues
            and guide customers through support conversations.
        </p>

    </div>
    """)


with col2:

    render_html("""
    <div class="feature-card">

        <div class="feature-icon">🎙️</div>

        <h3>AI Voice Assistant</h3>

        <p>
            Enable natural spoken conversations through
            a browser microphone and speaker.
        </p>

    </div>
    """)


with col3:

    render_html("""
    <div class="feature-card">

        <div class="feature-icon">☎️</div>

        <h3>AI Phone Agent</h3>

        <p>
            Connect customer calls to an AI agent
            and route complex cases to human support.
        </p>

    </div>
    """)


# ==========================================
# FOOTER
# ==========================================

render_html("""
<div class="footer">

    ✦ NEXA AI CUSTOMER SUPPORT PLATFORM

    <br><br>

    Built with Python • Streamlit • OpenAI • Make.com

    <br><br>

    © 2026 Nexa AI. All rights reserved.

</div>
""")
