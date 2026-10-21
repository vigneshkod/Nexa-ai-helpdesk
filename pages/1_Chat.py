import re
import streamlit as st

from database import initialize_database, get_all_tickets, get_ticket
from ticket_manager import create_ticket
from ai_agent import get_response


# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Nexa AI | Customer Support",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()


# ==========================================
# SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! Welcome to Nexa AI Support. 👋\n\n"
                "Describe your problem below. I can suggest basic steps "
                "and help you create a support ticket when needed."
            ),
        }
    ]

if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = None

if "lookup_ticket_id" not in st.session_state:
    st.session_state.lookup_ticket_id = ""

if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0

if "ticket_category" not in st.session_state:
    st.session_state.ticket_category = "Other"

if "category_widget_version" not in st.session_state:
    st.session_state.category_widget_version = 0


# ==========================================
# CUSTOM STYLING
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
    .chat-header {
        background: linear-gradient(120deg, #29234d, #172943);
        border: 1px solid #6556a1;
        border-radius: 20px;
        padding: 26px;
        margin-bottom: 24px;
    }
    .chat-header h1 {
        color: white;
        margin-bottom: 8px;
    }
    .chat-header p {
        color: #c1c9dc;
        font-size: 16px;
    }
    .ticket-card {
        background: #162c29;
        border: 1px solid #3a8068;
        border-radius: 15px;
        padding: 20px;
    }
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
    div[data-testid="stMetric"] {
        background: #182238;
        border: 1px solid #35415d;
        border-radius: 12px;
        padding: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# HEADER
# ==========================================
st.markdown(
    """
    <div class="chat-header">
        <h1>💬 Nexa AI Support Center</h1>
        <p>
            Your support, simplified. Describe your problem, get basic guidance,
            create a ticket, and track its progress in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# NAVIGATION
# ==========================================
nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")

with nav2:
    if st.button("📊 Admin Dashboard", use_container_width=True):
        st.info(
            "Open a separate VS Code terminal and run:\n\n"
            "`streamlit run admin_dashboard.py`"
        )

with nav3:
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! Welcome to Nexa AI Support. 👋\n\n"
                    "Describe your problem, and I'll guide you with basic "
                    "troubleshooting or support-ticket creation."
                ),
            }
        ]
        st.session_state.ticket_id = None
        st.session_state.ticket_category = "Other"
        st.session_state.category_widget_version += 1
        st.session_state.chat_input_key += 1
        st.rerun()

with nav4:
    if st.button("🎙️ Voice Support", use_container_width=True):
        st.switch_page("pages/2_Voice.py")


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.title("✦ NEXA AI")
    st.caption("CUSTOMER SUPPORT PLATFORM")
    st.divider()

    st.subheader("Support Channels")
    st.write("💬 Text Support — Available")
    st.write("🎙️ Browser Voice — Available")
    st.write("☎️ Phone Support — Coming soon")

    st.divider()
    st.subheader("What you can do")
    st.write("🎫 Create a support ticket")
    st.write("🔎 Track your ticket status")
    st.write("📋 View recent tickets")

    st.divider()
    st.caption(
        "Chat responses currently use a local rule-based response engine. "
        "OpenAI API calls are not required for this mode."
    )


# ==========================================
# CHAT CONVERSATION — CONNECTED TO ai_agent.py
# ==========================================
st.subheader("💬 Your Conversation")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input(
    "Describe your problem here...",
    key=f"chat_input_{st.session_state.chat_input_key}",
)

if user_input:
    cleaned_input = user_input.strip()

    if cleaned_input:
        st.session_state.messages.append(
            {"role": "user", "content": cleaned_input}
        )

        try:
            result = get_response(cleaned_input)

            # ai_agent.get_response() is expected to return a dictionary
            # with: reply, category, offer_ticket, and escalate.
            reply = result.get(
                "reply",
                "I'm sorry, I couldn't prepare a response. Please try again.",
            )
            category_result = result.get("category", "Other")
            valid_categories = [
                "Login / Account Issue",
                "Payment / Billing",
                "Technical Issue",
                "Order / Delivery",
                "Product Information",
                "Other",
            ]

            # Match the detected category to the form's exact dropdown option.
            category_result_text = str(category_result).strip().lower()
            category_match = next(
                (
                    option
                    for option in valid_categories
                    if option.lower() == category_result_text
                ),
                "Other",
            )
            st.session_state.ticket_category = category_match
            st.session_state.category_widget_version += 1
            category_result = category_match

            offer_ticket = result.get("offer_ticket", False)
            escalate = result.get("escalate", False)

            # Add clear next-step guidance without claiming the issue is fixed.
            if escalate:
                reply += (
                    "\n\n**Human support:** Your request should be reviewed "
                    "by a human support agent. You can submit the ticket form below."
                )
            elif offer_ticket:
                reply += (
                    "\n\n**Need more help?** You can submit the support ticket "
                    "form below so the support team can review your issue."
                )

            reply += f"\n\n*Suggested category: {category_result}*"

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        except Exception as error:
            # Keep the UI usable if ai_agent.py has an unexpected issue.
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "I'm sorry, I couldn't process that message right now. "
                        "You can still create a support ticket using the form below."
                    ),
                }
            )
            print("Nexa AI response error:", error)

        st.rerun()


# ==========================================
# CREATE SUPPORT TICKET
# ==========================================
st.divider()
st.subheader("🎫 Create a Support Ticket")
st.write(
    "Enter your details below. Your complaint will be recorded in the "
    "local support database and sent to your configured Make.com workflow."
)

with st.form("ticket_form", clear_on_submit=False):
    customer_name = st.text_input(
        "Customer Name",
        placeholder="Enter your name",
        max_chars=100,
    )

    customer_email = st.text_input(
        "Email Address (optional)",
        placeholder="you@example.com",
        max_chars=254,
    )

    category_options = [
        "Login / Account Issue",
        "Payment / Billing",
        "Technical Issue",
        "Order / Delivery",
        "Product Information",
        "Other",
    ]

    # A new widget key forces Streamlit to use the latest detected category,
    # rather than retaining an old dropdown selection from a previous message.
    category_default_index = category_options.index(
        st.session_state.ticket_category
    )

    category = st.selectbox(
        "Problem Category",
        category_options,
        index=category_default_index,
        key=f"ticket_category_{st.session_state.category_widget_version}",
    )

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High", "Urgent"],
        index=1,
    )

    description = st.text_area(
        "Describe Your Problem",
        placeholder="Explain what happened and what help you need...",
        height=140,
        max_chars=5000,
    )

    submitted = st.form_submit_button(
        "🎫 Create Support Ticket",
        use_container_width=True,
    )

    if submitted:
        name_value = customer_name.strip()
        email_value = customer_email.strip()
        description_value = description.strip()

        if not name_value:
            st.error("Please enter your name.")

        elif not description_value:
            st.error("Please describe your problem.")

        elif email_value and not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email_value,
        ):
            st.error("Please enter a valid email address.")

        else:
            try:
                new_ticket_id = create_ticket(
                    customer_name=name_value,
                    customer_email=email_value,
                    category=category,
                    priority=priority,
                    description=description_value,
                )

                st.session_state.ticket_id = new_ticket_id
                st.session_state.lookup_ticket_id = new_ticket_id

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "Your support ticket has been created! "
                            f"Your ticket ID is {new_ticket_id}. "
                            "Keep this ID to track your request."
                        ),
                    }
                )

                st.rerun()

            except Exception as error:
                print("Ticket creation error:", error)
                st.error(
                    "We couldn't create your ticket. Please try again. "
                    "If the problem continues, check the terminal for the error."
                )


# ==========================================
# TICKET CONFIRMATION
# ==========================================
if st.session_state.ticket_id:
    confirmed_ticket = get_ticket(st.session_state.ticket_id)

    if confirmed_ticket:
        st.divider()
        st.subheader("✅ Support Request Registered")
        st.success("Your support ticket was created successfully!")

        st.markdown(
            """
            <div class="ticket-card">
                <h3>Ticket Confirmation</h3>
                <p>Your request has been recorded.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("**Your Ticket ID**")
        st.code(confirmed_ticket["ticket_id"], language=None)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Current Status", confirmed_ticket["status"])
            st.write("**Category:**", confirmed_ticket["category"])

        with col2:
            st.write("**Priority:**", confirmed_ticket["priority"])
            st.write("**Created:**", confirmed_ticket["created_at"])

        st.info(
            "Save your ticket ID. Use it in the tracking section below "
            "to check the status stored in the local database."
        )


# ==========================================
# TRACK SUPPORT TICKET
# ==========================================
st.divider()
st.subheader("🔎 Track Your Support Ticket")
st.write(
    "Enter your ticket ID to view the latest status recorded in the support database."
)

with st.form("track_ticket_form"):
    lookup_id = st.text_input(
        "Ticket ID",
        value=st.session_state.lookup_ticket_id,
        placeholder="Example: NEXA-5B05DB56",
        max_chars=50,
    )

    track_submitted = st.form_submit_button(
        "🔍 Check Ticket Status",
        use_container_width=True,
    )

    if track_submitted:
        st.session_state.lookup_ticket_id = lookup_id.strip().upper()

        if not st.session_state.lookup_ticket_id:
            st.warning("Please enter your ticket ID.")
        else:
            st.rerun()

if st.session_state.lookup_ticket_id:
    tracked_ticket = get_ticket(st.session_state.lookup_ticket_id)

    if tracked_ticket:
        st.success("Ticket found!")
        st.write("**Ticket ID:**", tracked_ticket["ticket_id"])

        status = tracked_ticket["status"]
        status_col1, status_col2 = st.columns(2)

        with status_col1:
            st.metric("Current Status", status)

        with status_col2:
            st.write("**Category:**", tracked_ticket["category"])
            st.write("**Priority:**", tracked_ticket["priority"])

        if status == "Resolved":
            st.success(
                "Your ticket is marked as resolved. "
                "Please contact support again if you still need help."
            )
        elif status == "Closed":
            st.info("This ticket is closed.")
        elif status == "In Progress":
            st.info("The support team is working on your request.")
        else:
            st.warning("Your ticket is open and awaiting processing.")

        st.caption(
            "Status is read from the local support database. "
            "Refresh or check again to see subsequent changes."
        )

    else:
        st.error("Ticket not found. Please check the ID and try again.")


# ==========================================
# RECENT TICKETS
# ==========================================
st.divider()

with st.expander("📋 View Recent Support Tickets"):
    tickets = get_all_tickets()

    if tickets:
        for item in tickets[:10]:
            st.markdown(f"**{item['ticket_id']}**")
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Category:**", item["category"])
                st.write("**Priority:**", item["priority"])

            with col2:
                st.write("**Status:**", item["status"])
                st.write("**Channel:**", item["channel"])

            st.caption(f"Created: {item['created_at']}")
            st.divider()
    else:
        st.info("No support tickets have been created yet.")


# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("Nexa AI Support Center | Development Prototype")
