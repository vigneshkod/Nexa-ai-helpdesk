import re
import json
import html

import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text

from ai_agent import get_response
from database import initialize_database
from ticket_manager import create_ticket


# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Nexa AI | Voice Support",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()

CATEGORIES = [
    "Login / Account Issue",
    "Payment / Billing",
    "Technical Issue",
    "Order / Delivery",
    "Product Information",
    "Other",
]


# ==========================================
# SESSION STATE
# ==========================================
if "voice_messages" not in st.session_state:
    st.session_state.voice_messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! Welcome to Nexa AI Voice Support. 🎙️\n\n"
                "Click Start Speaking, allow microphone access, and describe "
                "your support issue in English. I'll respond using Nexa AI's "
                "current support engine."
            ),
        }
    ]

if "voice_category" not in st.session_state:
    st.session_state.voice_category = "Other"

if "voice_ticket_description" not in st.session_state:
    st.session_state.voice_ticket_description = ""

if "voice_ticket_id" not in st.session_state:
    st.session_state.voice_ticket_id = None


# ==========================================
# STYLING
# ==========================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #080d19, #131a2e);
        color: #ffffff;
    }
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .voice-header {
        background: linear-gradient(120deg, #29234d, #172943);
        border: 1px solid #6556a1;
        border-radius: 20px;
        padding: 26px;
        margin-bottom: 24px;
    }
    .voice-header h1 { color: white; margin-bottom: 8px; }
    .voice-header p { color: #c1c9dc; font-size: 16px; }
    [data-testid="stChatMessage"] {
        background: #192238;
        border: 1px solid #303d5c;
        border-radius: 15px;
        padding: 14px;
    }
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 11px;
        min-height: 42px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# HEADER / NAVIGATION
# ==========================================
st.markdown(
    """
    <div class="voice-header">
        <h1>🎙️ Nexa AI Voice Support</h1>
        <p>
            Speak about your issue, receive a support response, and create a
            ticket without needing OpenAI API credits.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

nav1, nav2 = st.columns(2)
with nav1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")
with nav2:
    if st.button("💬 Open Text Support", use_container_width=True):
        st.switch_page("pages/1_Chat.py")

st.info(
    "Privacy reminder: speech recognition may send audio to Google's speech "
    "recognition service. Please do not speak passwords, OTPs, full card "
    "numbers, or other sensitive information."
)


# ==========================================
# VOICE INPUT
# ==========================================
st.subheader("🎤 Speak to Nexa AI")
st.write(
    "Click **Start Speaking**, allow microphone access in your browser, "
    "say your issue in English, then click **Stop**."
)

try:
    transcribed_text = speech_to_text(
        language="en-US",
        start_prompt="🎙️ Start Speaking",
        stop_prompt="⏹️ Stop",
        just_once=True,
        use_container_width=True,
        key="nexa_voice_recognition",
    )
except Exception as error:
    transcribed_text = None
    st.error(
        "The microphone component could not start. Check the terminal for "
        "details, install the required package, and refresh the page."
    )
    print("Nexa voice recognition error:", error)

if transcribed_text:
    cleaned_text = transcribed_text.strip()
    if cleaned_text:
        st.session_state.voice_messages.append(
            {"role": "user", "content": cleaned_text}
        )
        # Prefill the ticket form with the latest spoken issue.
        st.session_state.voice_ticket_description = cleaned_text

        try:
            result = get_response(cleaned_text)
            if not isinstance(result, dict):
                raise TypeError("get_response() should return a dictionary.")

            reply = str(
                result.get(
                    "reply",
                    "I'm sorry, I couldn't prepare a response. Please try again.",
                )
            )
            detected_category = str(result.get("category", "Other")).strip()
            matched_category = next(
                (
                    option
                    for option in CATEGORIES
                    if option.casefold() == detected_category.casefold()
                ),
                "Other",
            )
            st.session_state.voice_category = matched_category

            if result.get("escalate", False):
                reply += (
                    "\n\n**Human support:** Your request should be reviewed "
                    "by a human support agent. You can create a ticket below."
                )
            elif result.get("offer_ticket", False):
                reply += (
                    "\n\n**Need more help?** Create a support ticket below "
                    "so the team can review your issue."
                )

            reply += f"\n\n*Suggested category: {matched_category}*"
            st.session_state.voice_messages.append(
                {"role": "assistant", "content": reply}
            )
        except Exception as error:
            print("Nexa voice agent error:", error)
            st.session_state.voice_messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "I'm sorry, I couldn't process that message. You can "
                        "still submit a support ticket below."
                    ),
                }
            )
        st.rerun()


# ==========================================
# VOICE CONVERSATION
# ==========================================
st.divider()
st.subheader("💬 Voice Conversation")
for message in st.session_state.voice_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

last_assistant_reply = next(
    (
        message["content"]
        for message in reversed(st.session_state.voice_messages)
        if message["role"] == "assistant"
    ),
    "Welcome to Nexa AI Voice Support.",
)

# Browser-native text-to-speech; no extra API key is needed.
safe_reply_json = json.dumps(last_assistant_reply, ensure_ascii=False).replace("</", "<\\/")
html_block = f"""
<div style="font-family: Arial, sans-serif; display:flex; gap:10px; flex-wrap:wrap;">
  <button id="speak-response" style="background:#5b4bdb;color:white;border:0;border-radius:10px;padding:11px 16px;cursor:pointer;font-size:14px;">
    🔊 Speak Latest Response
  </button>
  <button id="stop-response" style="background:#26334d;color:white;border:1px solid #53627f;border-radius:10px;padding:11px 16px;cursor:pointer;font-size:14px;">
    ⏹ Stop Audio
  </button>
  <span id="speech-status" style="color:#64748b;align-self:center;font-size:13px;"></span>
</div>
<script>
  const responseText = {safe_reply_json};
  const speakButton = document.getElementById('speak-response');
  const stopButton = document.getElementById('stop-response');
  const status = document.getElementById('speech-status');
  speakButton.addEventListener('click', () => {{
    if (!('speechSynthesis' in window)) {{
      status.textContent = 'Speech playback is not supported by this browser.';
      return;
    }}
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(responseText);
    utterance.lang = 'en-US';
    utterance.rate = 1;
    utterance.onstart = () => status.textContent = 'Speaking…';
    utterance.onend = () => status.textContent = 'Finished';
    utterance.onerror = () => status.textContent = 'Could not play speech.';
    window.speechSynthesis.speak(utterance);
  }});
  stopButton.addEventListener('click', () => {{
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    status.textContent = 'Stopped';
  }});
</script>
"""
components.html(html_block, height=64, scrolling=False)


# ==========================================
# CREATE SUPPORT TICKET FROM VOICE ISSUE
# ==========================================
st.divider()
st.subheader("🎫 Create a Support Ticket")
st.write(
    "The latest spoken message is copied into the description. Review it "
    "and edit any details before submitting."
)

with st.form("voice_ticket_form", clear_on_submit=False):
    customer_name = st.text_input(
        "Customer Name",
        placeholder="Enter your name",
        max_chars=100,
        key="voice_customer_name",
    )
    customer_email = st.text_input(
        "Email Address (optional)",
        placeholder="you@example.com",
        max_chars=254,
        key="voice_customer_email",
    )
    category = st.selectbox(
        "Problem Category",
        CATEGORIES,
        key="voice_category",
    )
    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High", "Urgent"],
        index=1,
        key="voice_ticket_priority",
    )
    description = st.text_area(
        "Describe Your Problem",
        height=130,
        max_chars=5000,
        key="voice_ticket_description",
        placeholder="Speak your issue above or type a description here...",
    )
    ticket_submitted = st.form_submit_button(
        "🎫 Create Support Ticket",
        use_container_width=True,
    )

if ticket_submitted:
    name_value = customer_name.strip()
    email_value = customer_email.strip()
    description_value = description.strip()

    if not name_value:
        st.error("Please enter your name.")
    elif not description_value:
        st.error("Please speak your issue above or type a description.")
    elif email_value and not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email_value
    ):
        st.error("Please enter a valid email address.")
    else:
        try:
            created_ticket_id = create_ticket(
                customer_name=name_value,
                customer_email=email_value,
                category=category,
                priority=priority,
                description=description_value,
            )
            st.session_state.voice_ticket_id = created_ticket_id
            st.success("Your voice support ticket was created successfully!")
        except Exception as error:
            print("Voice ticket creation error:", error)
            st.error(
                "We couldn't create the ticket. Check the VS Code terminal "
                "for details and try again."
            )

if st.session_state.voice_ticket_id:
    st.markdown("**Your Ticket ID**")
    st.code(st.session_state.voice_ticket_id, language=None)
    st.info(
        "Keep this ID to track your ticket. The ticket is saved through the "
        "same ticket manager used by Text Support."
    )


# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("Nexa AI Voice Support | Browser speech prototype")
