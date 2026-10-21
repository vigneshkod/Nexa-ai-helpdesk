
import streamlit as st
from datetime import datetime

from text_chat import get_ai_response

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Nexa AI | Customer Support",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>

/* Main application */
.stApp {
    background: linear-gradient(135deg, #0b1020, #11162b);
    color: #f5f5fa;
}

/* Hide Streamlit branding */
#MainMenu, footer {
    visibility: hidden;
}

/* Main content */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #11172b;
    border-right: 1px solid #29314c;
}

section[data-testid="stSidebar"] * {
    color: #e8eaff;
}

/* Main heading */
.main-title {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff, #a99cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}

.subtitle {
    color: #a4acc5;
    font-size: 15px;
}

/* Status */
.status-card {
    background: #17243a;
    border: 1px solid #294c60;
    padding: 12px 16px;
    border-radius: 14px;
    color: #b7e9d1;
    font-size: 13px;
}

/* Welcome section */
.welcome-card {
    background: linear-gradient(135deg, #25244c, #30265a, #182747);
    border: 1px solid #554b91;
    border-radius: 22px;
    padding: 32px;
    margin-top: 25px;
    margin-bottom: 22px;
}

.welcome-title {
    color: white;
    font-size: 27px;
    font-weight: 750;
}

.welcome-text {
    color: #d0d0ee;
    font-size: 15px;
    line-height: 1.7;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #171e32;
    border: 1px solid #293451;
    border-radius: 17px;
    padding: 14px;
    margin-bottom: 12px;
}

/* Chat input */
[data-testid="stChatInput"] {
    border: 1px solid #7864ce;
    border-radius: 18px;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: 1px solid #6554a8;
    background: #222344;
    color: white;
    min-height: 45px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #493b80;
    border-color: #a18bff;
    color: white;
    transform: translateY(-2px);
}

/* Section headings */
.section-heading {
    color: #e7e4ff;
    font-size: 19px;
    font-weight: 700;
    margin-top: 22px;
    margin-bottom: 12px;
}

/* Footer */
.custom-footer {
    text-align: center;
    color: #777f9d;
    font-size: 12px;
    margin-top: 45px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------
# SESSION STATE
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "last_error" not in st.session_state:
    st.session_state.last_error = None


# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:20px 5px;">
        <div style="font-size:55px;">🎧</div>
        <h2 style="margin-bottom:0;">NEXA AI</h2>
        <p style="color:#9ba4c2;">Customer Support Center</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 💬 Conversation")

    st.write(f"Messages: {len(st.session_state.messages)}")

    if st.button("➕ New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_error = None
        st.session_state.pending_prompt = None
        st.rerun()

    st.divider()

    st.markdown("### 🎯 Support Channels")

    st.markdown("""
    - 💬 Text Chat — Interface available
    - 🎙️ Browser Voice — Coming next
    - ☎️ Phone Support — Coming next
    """)

    st.divider()

    st.markdown("### ⚙️ System Information")

    st.markdown("""
    **Platform:** Nexa AI Help Desk

    **Backend:** Python

    **Interface:** Streamlit

    **Database:** SQLite

    **Automation:** Make.com
    """)

    st.info(
        "AI responses require available OpenAI API credits. "
        "The interface can still be explored without credits."
    )


# -------------------------------
# HEADER
# -------------------------------

header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown(
        '<div class="main-title">Nexa AI Help Desk</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your intelligent customer support assistant</div>',
        unsafe_allow_html=True
    )

with header_col2:
    st.markdown("""
    <div class="status-card">
        🎧 &nbsp; AI SUPPORT
        <br>
        <b>Text channel</b>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
# WELCOME SCREEN
# -------------------------------

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome-card">
        <div style="font-size:42px;">🤖</div>
        <div class="welcome-title">
            Hello! How can I help you today?
        </div>
        <div class="welcome-text">
            Welcome to Nexa AI Customer Support.
            Describe your issue, ask a question, or select
            one of the suggestions below to get started.
        </div>
        <br>
        <span style="color:#c6baff;">
            ✦ Intelligent support &nbsp; ✦ Simple conversations
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">✨ Quick Support Suggestions</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔐  Login and Account Issues",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "I am unable to log in to my account. "
                "Can you help me?"
            )
            st.rerun()

        if st.button(
            "💳  Payment Problems",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "My payment was deducted but the "
                "transaction failed. What should I do?"
            )
            st.rerun()

    with col2:
        if st.button(
            "🌐  Internet and Technical Support",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "My internet connection is not working. "
                "Please help me."
            )
            st.rerun()

        if st.button(
            "📦  Order and Delivery Issues",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "My order has not been delivered yet. "
                "Can you help me?"
            )
            st.rerun()


# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------

else:

    st.markdown(
        '<div class="section-heading">💬 Your Conversation</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            if message["role"] == "assistant":
                st.markdown(message["content"])
            else:
                st.write(message["content"])


# -------------------------------
# CUSTOMER MESSAGE INPUT
# -------------------------------

user_input = st.chat_input(
    "✍️ Type your message here..."
)

# Handle either typed message or suggestion button
prompt = st.session_state.pending_prompt

if prompt:
    st.session_state.pending_prompt = None

elif user_input:
    prompt = user_input


# -------------------------------
# AI RESPONSE
# -------------------------------

if prompt:

    st.session_state.last_error = None

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Nexa AI is thinking..."):

            try:

                answer = get_ai_response(
                    st.session_state.messages
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.session_state.last_error = str(error)

                st.warning(
                    "Our AI response service is currently unavailable. "
                    "Please try again later."
                )

                st.caption(
                    "Check your OpenAI API credits and configuration."
                )


# -------------------------------
# ERROR DETAILS
# -------------------------------

if st.session_state.last_error:

    with st.expander("Technical error details"):
        st.code(st.session_state.last_error)


# -------------------------------
# FOOTER
# -------------------------------

st.markdown("""
<div class="custom-footer">
    NEXA AI CUSTOMER SUPPORT PLATFORM
    <br>
    Built with Python • Streamlit • OpenAI
    <br><br>
    © 2026 Nexa AI Help Desk
</div>
""", unsafe_allow_html=True)
