
from database import get_connection, initialize_database
from datetime import datetime
from dotenv import load_dotenv
import os
import uuid
import requests

load_dotenv()

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")


def create_ticket(
    customer_name,
    customer_email,
    category,
    priority,
    description
):
    initialize_database()

    ticket_id = "NEXA-" + uuid.uuid4().hex[:8].upper()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Save the ticket locally first
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO tickets (
                ticket_id, customer_name, customer_email,
                category, priority, description,
                channel, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            customer_name,
            customer_email,
            category,
            priority,
            description,
            "Text Chat",
            "Open",
            created_at
        ))

        connection.commit()

    finally:
        connection.close()

    # 2. Send the ticket to Make.com
    if MAKE_WEBHOOK_URL:
        payload = {
            "ticket_id": ticket_id,
            "customer": customer_name,
            "customer_email": customer_email or "",
            "category": category,
            "priority": priority,
            "description": description,
            "status": "Open",
            "channel": "Text Chat",
            "created_at": created_at
        }

        try:
            response = requests.post(
                MAKE_WEBHOOK_URL,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            print("Ticket sent to Make.com successfully.")

        except requests.RequestException as error:
            print(
                "Ticket saved locally, but Make.com delivery failed:",
                error
            )

    else:
        print("MAKE_WEBHOOK_URL is not configured.")

    # 3. Return the ticket ID to the chat page
    return ticket_id
