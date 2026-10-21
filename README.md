# 🤖 Nexa AI — Customer Support Automation System

Nexa AI is a Python and Streamlit-based customer support application that helps automate customer queries, issue categorization, ticket management, and support workflows.

## ✨ Features

- 💬 **Text Support:** Responds to customer queries using rule-based logic.
- 🎙️ **Voice Support:** Browser-based voice input and spoken responses.
- 🏷️ **Issue Categorization:** Identifies support categories such as payment and billing.
- 🎫 **Ticket Management:** Creates and tracks customer support tickets.
- 📊 **Admin Dashboard:** View and manage support tickets and their statuses.
- 📧 **Email Notifications:** Automates notifications through Make.com and Gmail.
- 📑 **Google Sheets Integration:** Syncs ticket details and status updates through Make.com.
- 🗄️ **Database Management:** Stores ticket records using SQLite.

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Make.com
- Google Sheets
- Gmail
- Browser Speech Recognition and Text-to-Speech

## 📁 Project Structure

```text
Nexa-ai-helpdesk/
├── Home.py
├── app.py
├── admin_dashboard.py
├── ai_agent.py
├── database.py
├── ticket_manager.py
├── text_chat.py
├── test_ai_agent.py
├── pages/
│   ├── 1_Chat.py
│   └── 2_Voice.py
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vigneshkod/Nexa-ai-helpdesk.git
cd Nexa-ai-helpdesk
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run Home.py
```

Open the local URL displayed in your terminal.

## ⚙️ Integrations

The application can connect with Make.com workflows to send ticket information to Google Sheets and trigger email notifications. These features require valid webhook and service configurations.

## 🔒 Security

- Keep API keys, passwords, and webhook URLs in local environment variables.
- Never commit `.env` files or credentials to GitHub.
- Use sample data instead of real customer information in public demonstrations.

## 🚧 Future Improvements

- Integrate a generative AI model for more natural responses.
- Add a knowledge base for answering questions from support documents.
- Integrate telephone-based customer support.
- Improve analytics and reporting.

## 👨‍💻 Author

**vigneshkod**

GitHub: [@vigneshkod](https://github.com/vigneshkod)
