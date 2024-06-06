# HCNB News Bot

## Description

HCNB News Bot fetches the latest news from various RSS feeds and sends them to a Telegram chat.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/cahsun147/HCNB.git
    cd HCNB
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project directory and add your Telegram bot token and chat ID:

    ```env
    TOKEN=your-telegram-bot-token
    CHAT_ID=your-chat-id
    ```

5. Run the bot:

    ```bash
    python hcnb.py
    ```

## Logging

The bot logs its activities in `output.log` located in the project directory.

## Updating the Repository

To update the repository with your latest changes:

1. Stage your changes:

    ```bash
    git add .
    ```

2. Commit your changes:

    ```bash
    git commit -m "Your commit message"
    ```

3. Push your changes to GitHub:

    ```bash
    git push https://cahsun147:your-personal-access-token@github.com/cahsun147/HCNB.git main
    ```

Make sure to replace `your-telegram-bot-token`, `your-chat-id`, and `your-personal-access-token` with your actual values.
