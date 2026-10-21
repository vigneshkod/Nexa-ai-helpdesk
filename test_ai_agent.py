
from ai_agent import get_response

test_messages = [
    "Hello",
    "I cannot log in to my account",
    "My payment was deducted twice",
    "My order has not arrived",
    "The application is showing an error",
    "I want to speak to a human agent",
]

for message in test_messages:
    result = get_response(message)

    print("\nCustomer:", message)
    print("Nexa AI:", result["reply"])
    print("Category:", result["category"])
    print("Offer ticket:", result["offer_ticket"])
    print("Escalate:", result["escalate"])
