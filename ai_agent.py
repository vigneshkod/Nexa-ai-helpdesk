"""
Nexa AI rule-based customer support engine.

This version works locally and does not call a paid AI API.
It returns:
    reply: response shown to the customer
    category: suggested ticket category
    offer_ticket: whether to suggest ticket creation
    escalate: whether human support is requested/recommended
"""

import re


SYSTEM_PROMPT = """
You are Nexa AI, a polite customer support assistant.
Provide safe, practical first-step guidance.
Never ask for passwords, OTPs, full card numbers, or secret keys.
Do not claim that an issue is fixed without customer confirmation.
Do not invent company policies, refund guarantees, delivery dates, or account details.
Recommend human support for account security, suspected fraud, repeated failures,
complaints, or when the customer asks for a human.
This prototype uses local rules, not a generative AI model.
"""


CATEGORY_RULES = [
    (
        "Login / Account Issue",
        [
            "login", "log in", "sign in", "signin", "password",
            "forgot password", "reset password", "locked out",
            "account locked", "otp", "verification code", "verification",
            "can't access account", "cannot access account",
        ],
    ),
    (
        "Payment / Billing",
        [
            "payment", "paid", "billing", "bill", "charged",
            "double charged", "charged twice", "deducted", "refund",
            "transaction", "invoice", "upi", "card declined",
        ],
    ),
    (
        "Order / Delivery",
        [
            "order", "delivery", "delivered", "shipment", "shipping",
            "tracking", "late", "not arrived", "not received",
            "missing package", "courier",
        ],
    ),
    (
        "Product Information",
        [
            "product", "feature", "features", "price", "pricing",
            "available", "availability", "specification", "specs",
            "how does it work",
        ],
    ),
    (
        "Technical Issue",
        [
            "error", "bug", "crash", "crashing", "not working",
            "doesn't work", "does not work", "broken", "slow",
            "loading", "blank screen", "freeze", "frozen",
            "install", "installation", "update", "website",
            "application", "app", "technical", "connection",
        ],
    ),
]


def normalize_message(message):
    """Normalize customer text for simple rule matching."""
    return re.sub(r"\s+", " ", str(message).lower()).strip()


def contains_any(message, phrases):
    """Return True if any phrase occurs in the normalized message."""
    return any(phrase in message for phrase in phrases)


def get_category(message):
    """Return the most likely support category for a message."""
    text = normalize_message(message)

    for category, keywords in CATEGORY_RULES:
        if contains_any(text, keywords):
            return category

    return "Other"


def get_response(message):
    """
    Return a response dictionary for the Streamlit chat interface.
    This is rule-based and does not use an OpenAI API call.
    """
    text = normalize_message(message)

    result = {
        "reply": "",
        "category": get_category(text),
        "offer_ticket": False,
        "escalate": False,
    }

    if not text:
        result["reply"] = "Please type a message so I can try to help."
        return result

    # Human-agent requests should be handled before other rules.
    human_phrases = [
        "human", "real person", "live agent", "support agent",
        "speak to someone", "talk to someone", "representative",
        "customer care", "human agent", "talk to a person",
    ]
    if contains_any(text, human_phrases):
        result.update(
            reply=(
                "I understand you'd like help from a human support agent. "
                "I can't transfer you directly from this demo, but you can "
                "submit the support ticket form below so the team can review "
                "your request. Please include a short description of the issue."
            ),
            offer_ticket=True,
            escalate=True,
        )
        return result

    # Security-sensitive concerns.
    security_phrases = [
        "hacked", "account hacked", "fraud", "scam", "stolen account",
        "unauthorized payment", "unauthorised payment", "someone accessed",
        "suspicious login", "identity theft",
    ]
    if contains_any(text, security_phrases):
        result.update(
            reply=(
                "This may be a security-sensitive issue. If you can safely "
                "access your account, use the service's official security "
                "settings to secure it and contact the official support team "
                "or your bank immediately if money may be at risk. Do not "
                "share passwords, OTPs, or full payment details here. "
                "I recommend creating a support ticket for human review."
            ),
            category="Login / Account Issue"
            if contains_any(text, ["hacked", "account", "login"])
            else "Payment / Billing",
            offer_ticket=True,
            escalate=True,
        )
        return result

    # Greetings and small talk.
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    if text in greetings or text in ["hello there", "hi there"]:
        result["reply"] = (
            "Hello! 👋 I'm Nexa AI Support. I can help with login problems, "
            "payments, orders, product questions, and technical issues. "
            "What do you need help with?"
        )
        return result

    if contains_any(text, ["thank you", "thanks", "thank you so much", "thx"]):
        result["reply"] = (
            "You're welcome! 😊 If you still need help, describe the issue "
            "or submit a support ticket below."
        )
        return result

    if contains_any(text, ["bye", "goodbye", "see you"]):
        result["reply"] = (
            "Goodbye! Thanks for contacting Nexa AI Support. If you need "
            "more help later, you can return here and create a support ticket."
        )
        return result

    # Login and account issues.
    if result["category"] == "Login / Account Issue":
        result.update(
            reply=(
                "I'm sorry you're having an account or login problem. Try these steps:\n\n"
                "1. Check that your email address or username is correct.\n"
                "2. Use the service's official password-reset option if available.\n"
                "3. Check your internet connection and try again.\n"
                "4. If a verification code is required, request a new one through "
                "the official service.\n\n"
                "Never share your password or OTP with anyone. If the issue "
                "continues, tell me what error message appears without sharing "
                "private information."
            ),
            offer_ticket=True,
        )
        if contains_any(text, ["hacked", "locked", "unauthorized", "unauthorised"]):
            result["escalate"] = True
        return result

    # Payments and billing.
    if result["category"] == "Payment / Billing":
        result.update(
            reply=(
                "I can help you investigate a payment or billing problem:\n\n"
                "1. Check your bank or payment app for the transaction status.\n"
                "2. Check whether the payment is pending, successful, or reversed.\n"
                "3. Keep the transaction reference and date for the support team, "
                "but don't post full account or card details here.\n\n"
                "If you were charged twice or the payment looks unauthorized, "
                "contact your bank or payment provider through its official channel. "
                "I can't confirm a refund from this demo."
            ),
            offer_ticket=True,
        )
        if contains_any(text, ["double charged", "charged twice", "deducted twice", "fraud", "unauthorized", "unauthorised"]):
            result["escalate"] = True
        return result

    # Orders and delivery.
    if result["category"] == "Order / Delivery":
        result.update(
            reply=(
                "Let's check your order issue:\n\n"
                "1. Open the service's official order-history page.\n"
                "2. Check the latest tracking status and estimated delivery details "
                "shown there.\n"
                "3. Confirm that the delivery address is correct.\n\n"
                "I can't access live order records from this demo. If the tracking "
                "hasn't updated or the order is late or missing, create a ticket "
                "and include the order reference without sensitive payment details."
            ),
            offer_ticket=True,
        )
        if contains_any(text, ["missing", "not arrived", "not received", "delivered but"]):
            result["escalate"] = True
        return result

    # Product questions: do not invent catalog facts.
    if result["category"] == "Product Information":
        result.update(
            reply=(
                "I can help clarify what information you need. Are you asking "
                "about a product's features, price, availability, or how to use it? "
                "I don't have access to a live product catalogue in this demo, "
                "so please check the official product page for current details."
            ),
            offer_ticket=False,
        )
        return result

    # Technical issues.
    if result["category"] == "Technical Issue":
        result.update(
            reply=(
                "I'm sorry you're experiencing a technical issue. Try these "
                "basic checks:\n\n"
                "1. Refresh the page or restart the application.\n"
                "2. Check your internet connection.\n"
                "3. If appropriate, update the app or try another browser.\n"
                "4. Note the exact error message and when it occurs.\n\n"
                "Please share the error text without passwords, OTPs, or private "
                "information. If the problem continues, I recommend a support ticket."
            ),
            offer_ticket=True,
        )
        if contains_any(text, ["crash", "crashing", "repeatedly", "every time"]):
            result["escalate"] = True
        return result

    # Explicit ticket requests.
    if contains_any(text, ["create a ticket", "raise a ticket", "support ticket", "register a complaint"]):
        result.update(
            reply=(
                "Of course. Please complete the support ticket form below with "
                "your name, a category, priority, and a description of the issue. "
                "After submission, Nexa AI will show your ticket ID."
            ),
            offer_ticket=True,
        )
        return result

    # Safe fallback for anything not recognized.
    result.update(
        reply=(
            "I want to help. Could you share a little more detail?\n\n"
            "For example:\n"
            "- What were you trying to do?\n"
            "- What happened instead?\n"
            "- Did you see an error message?\n\n"
            "Please don't include passwords, OTPs, or other sensitive information. "
            "If you prefer, you can submit a support ticket using the form below."
        ),
        offer_ticket=True,
    )
    return result
