
import os
from pathlib import Path

import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv

from database import initialize_database, get_all_tickets, get_connection


# -------------------------------
# ENVIRONMENT CONFIGURATION
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

MAKE_STATUS_WEBHOOK_URL = os.getenv("MAKE_STATUS_WEBHOOK_URL", "").strip()


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Nexa AI | Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

initialize_database()


# -------------------------------
# CUSTOM DESIGN
# -------------------------------

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: white;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

[data-testid="stMetric"] {
    background: #182238;
    border: 1px solid #35415d;
    padding: 18px;
    border-radius: 15px;
}

[data-testid="stMetricValue"] {
    color: #b5a4ff;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# STATUS SYNC FUNCTION
# -------------------------------

def sync_status_to_make(ticket_id, new_status):
    """
    Send the updated ticket status to Make.com.
    The local database update is completed separately.
    """

    if not MAKE_STATUS_WEBHOOK_URL:
        st.warning(
            "Status saved locally, but Google Sheets sync was skipped. "
            "MAKE_STATUS_WEBHOOK_URL is missing from your .env file."
        )
        return False

    payload = {
        "ticket_id": ticket_id,
        "status": new_status
    }

    try:
        response = requests.post(
            MAKE_STATUS_WEBHOOK_URL,
            json=payload,
            timeout=15
        )
        response.raise_for_status()

        return True

    except requests.RequestException:
        st.warning(
            "Status saved in the local database, but Make.com could not "
            "confirm delivery. Check your webhook and Make.com scenario."
        )
        return False


# -------------------------------
# HEADER
# -------------------------------

st.title("📊 Nexa AI — Admin Dashboard")
st.caption("Customer Support Operations Center")

col1, col2 = st.columns([1, 5])

with col1:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")

with col2:
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

st.divider()


# -------------------------------
# LOAD TICKETS
# -------------------------------

tickets = [dict(ticket) for ticket in get_all_tickets()]

if not tickets:
    st.info(
        "No tickets found. Create a ticket from the customer chat page."
    )
    st.stop()

df = pd.DataFrame(tickets)


# -------------------------------
# SUMMARY METRICS
# -------------------------------

total_tickets = len(df)
open_tickets = int((df["status"] == "Open").sum())
progress_tickets = int((df["status"] == "In Progress").sum())
high_priority = int(df["priority"].isin(["High", "Urgent"]).sum())

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Tickets", total_tickets)
c2.metric("Open Tickets", open_tickets)
c3.metric("In Progress", progress_tickets)
c4.metric("High / Urgent", high_priority)

st.divider()


# -------------------------------
# SEARCH AND FILTERS
# -------------------------------

st.subheader("🔎 Search and Filter Tickets")

search = st.text_input(
    "Search by ticket ID, customer or description"
)

f1, f2, f3 = st.columns(3)

with f1:
    status_filter = st.selectbox(
        "Status",
        ["All", "Open", "In Progress", "Resolved", "Closed"]
    )

with f2:
    priority_filter = st.selectbox(
        "Priority",
        ["All", "Low", "Medium", "High", "Urgent"]
    )

with f3:
    category_options = ["All"] + sorted(
        df["category"].dropna().unique().tolist()
    )

    category_filter = st.selectbox(
        "Category",
        category_options
    )

filtered = df.copy()

if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]

if priority_filter != "All":
    filtered = filtered[filtered["priority"] == priority_filter]

if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]

if search.strip():
    searchable = (
        filtered["ticket_id"].fillna("").astype(str)
        + " "
        + filtered["customer_name"].fillna("").astype(str)
        + " "
        + filtered["description"].fillna("").astype(str)
    )

    filtered = filtered[
        searchable.str.contains(
            search.strip(),
            case=False,
            regex=False
        )
    ]


# -------------------------------
# TICKET TABLE
# -------------------------------

st.subheader("🎫 Support Tickets")

st.caption(f"Showing {len(filtered)} of {len(df)} tickets")

display_columns = [
    "ticket_id",
    "customer_name",
    "category",
    "priority",
    "channel",
    "status",
    "created_at"
]

st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True
)


# -------------------------------
# TICKET DETAILS
# -------------------------------

st.divider()
st.subheader("📄 Ticket Details")

ticket_ids = df["ticket_id"].tolist()

selected_id = st.selectbox(
    "Select a ticket",
    ticket_ids
)

ticket = next(
    item for item in tickets
    if item["ticket_id"] == selected_id
)

left, right = st.columns(2)

with left:
    st.write("**Customer:**", ticket["customer_name"])
    st.write(
        "**Email:**",
        ticket["customer_email"] or "Not provided"
    )
    st.write("**Category:**", ticket["category"])

with right:
    st.write("**Priority:**", ticket["priority"])
    st.write("**Channel:**", ticket["channel"])
    st.write("**Current status:**", ticket["status"])

st.markdown("**Customer complaint:**")
st.write(ticket["description"])
st.caption("Created: " + ticket["created_at"])


# -------------------------------
# UPDATE TICKET STATUS
# -------------------------------

st.divider()
st.subheader("⚙️ Update Ticket Status")

statuses = ["Open", "In Progress", "Resolved", "Closed"]

current_status = ticket["status"]

default_index = (
    statuses.index(current_status)
    if current_status in statuses
    else 0
)

with st.form("update_status_form"):

    new_status = st.selectbox(
        "Choose the new status",
        statuses,
        index=default_index
    )

    save_status = st.form_submit_button(
        "Save Status",
        use_container_width=True
    )

    if save_status:

        if new_status == current_status:
            st.info(
                f"Ticket {selected_id} already has status "
                f"{current_status}. No change was made."
            )

        else:
            connection = get_connection()

            try:
                connection.execute(
                    """
                    UPDATE tickets
                    SET status = ?
                    WHERE ticket_id = ?
                    """,
                    (new_status, selected_id)
                )
                connection.commit()

            finally:
                connection.close()

            # The local status is saved first.
            st.success(
                f"Ticket {selected_id} saved locally as {new_status}."
            )

            # Then notify Make.com to update Google Sheets.
            if sync_status_to_make(selected_id, new_status):
                st.success(
                    "Google Sheets sync request sent successfully."
                )

            st.rerun()


# -------------------------------
# FOOTER
# -------------------------------

st.divider()
st.caption("Nexa AI Support Operations | Development Prototype")
