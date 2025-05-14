# Personal Task Reminder Chatbot

A conversational AI chatbot built with [RASA](https://rasa.com/) for setting and managing task reminders, integrated with a static JavaScript frontend hosted on [GitHub Pages](https://pages.github.com/), [Appwrite](https://appwrite.io/) for backend services, and a Streamlit app for an alternative web interface. The chatbot allows users to set reminders (e.g., "remind me to call Mom tomorrow"), view reminders, and receive automatic notifications for due tasks. This project was developed as a portfolio piece to demonstrate skills in conversational AI, backend-as-a-service (BaaS), and full-stack development.

## Features

- **Set Reminders:** Create reminders with natural language (e.g., "remind me to buy groceries at 6 PM").
- **View Reminders:** List all reminders with due status (e.g., "show my reminders").
- **Automatic Notifications:** Receive notifications for due reminders locally.
- **Virtual Environment:** Managed with [uv](https://docs.astral.sh/uv/) for reproducible dependency installation.

## Tech Stack

- **RASA (<=3.8):** Conversational AI framework for intent recognition and dialogue management.
- **Python 3.10:** Core programming language, compatible with RASA <=3.8.
- **uv:** Virtual environment and package manager for dependency management.

## Repository Structure

```
Reminder_ChatBot/
├── data/                    # RASA training data
│   ├── nlu.yml             # NLU training examples
│   ├── rules.yml           # Dialogue rules
│   └── stories.yml         # Dialogue stories
├── actions.py              # RASA custom actions
├── domain.yml              # RASA domain configuration
├── endpoints.yml           # RASA endpoints configuration
├── reminder_scheduler.py   # Local reminder scheduler
├── requirements.txt        # Dependencies for uv
├── README.md               # This file
└── config.yml              # RASA configuration
```

## Prerequisites

- **Python 3.10:** Ensure Python 3.10 is installed ([download](https://www.python.org/downloads/)).
- **uv:** Install uv for virtual environment management ([instructions](https://docs.astral.sh/uv/)).
- **GitHub Account:** For hosting the frontend on GitHub Pages.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Saber0722/Reminder_ChatBot.git
cd Reminder_ChatBot
```

### 2. Set Up Virtual Environment with uv
This project uses **uv** to manage dependencies in a Python 3.10 virtual environment. All packages were added using `uv add`, and the lock file ensures reproducibility.

```bash
# Create and activate virtual environment
uv venv --python 3.10
source .venv/bin/activate  # On Windows:. \.venv\Scripts\activate

# Install dependencies
uv sync
```

This installs all required libraries, including `rasa<=3.8`, `python-dateutil`, and others listed in `requirements.txt`.

### 3. Train the RASA Model
```bash
rasa train
```

This generates a model in the `models/` directory based on `data/nlu.yml`, `data/rules.yml`, `data/stories.yml`, and `domain.yml`.

## Running the Chatbot Locally

The chatbot requires three separate terminal processes: one for RASA actions, one for the RASA shell, and one for the reminder scheduler. Ensure the virtual environment is activated in each terminal (`source .venv/bin/activate`).

### Terminal 1: RASA Action Server
```bash
rasa run actions
```
- Runs custom actions in `actions.py` (e.g., `action_save_reminder`, `action_view_reminders`).
- Listens on `http://localhost:5055`.

### Terminal 2: RASA Shell
```bash
rasa shell
```
- Starts an interactive CLI for testing the chatbot.
- Processes user inputs (e.g., “remind me to call Mom tomorrow”) and triggers actions.
- Use this to test intents and dialogue flows.

### Terminal 3: Reminder Scheduler
```bash
python reminder_scheduler.py
```
- Runs a background process to check `reminders.json` every minute for due reminders.
- Prints notifications (e.g., “Reminder: call Mom is due now!”) to the console.
 
### Testing Locally
- In the RASA shell (Terminal 2), try:
  - “hi” → “Hi! I'm your reminder bot. How can I help you?”
  - “remind me to call Mom in 2 minutes” → “Got it! Reminder set for 'call Mom' at '2025-05-15T00:47:00+05:30'.”
  - “show my reminders” → Lists reminders with due status.
- In Terminal 3, wait 2 minutes to see the scheduler print a notification (e.g., at 12:47 AM IST, May 15, 2025).

## Troubleshooting

- **RASA Not Responding:**
  - Ensure `rasa run actions` and `rasa run --enable-api` are running.
- **Scheduler Issues:**
  - Confirm `reminders.json` (local)
  - Test with reminders set for “in 5 minutes” (e.g., 12:50 AM IST).
- **uv Sync Fails:**
  - Ensure Python 3.10 is installed and uv is updated (`uv --version`).
  - Run `uv sync --frozen` to use locked dependencies.

## License

MIT License. See [LICENSE](LICENSE) for details.
