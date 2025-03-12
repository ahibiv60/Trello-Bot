# Trello Bot
Trello Bot is a bot that sends notifications to Discord about cards added to Trello. It automates the process of monitoring new cards and tagging relevant users.

## Features
- Checks cards in Trello via API.
- Sends messages to Discord via webhook.
- Tags specific users for certain events (e.g., Approved messages).

## Requirements
Before running the project, make sure you have installed:
- **Python 3.13.2** (recommended)
- **pip** (Python package manager)

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/Trello-Bot.git
   ```
2. **Navigate to the project folder:**
   ```bash
   cd Trello-Bot
   ```
3. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Before running the bot for the first time, configure the necessary files.

### Configuring `config.env`
The `config.env` file contains the project's main settings. Before using it remove `_example` from the filename:

**In `config.env`, specify:**
- `ENVIRONMENT` – should be "main".
- `TRELLO_KEY` – API key for Trello access.
- `TRELLO_TOKEN` – Trello account token.
- `READY_LIST_ID` – ID of the Ready to be checked issues list in Trello.
- `APPROVED_LIST_ID` – ID of the Approved issues list in Trello.
- `DISCORD_WEBHOOK_URL_MAIN` – URL of the Discord webhook created in certain channel.
- `DISCORD_WEBHOOK_URL_TEST` – should be empty.

### Configuring `resources/users.json`
The `resources/users.json` file contains a list of users who will be tagged when sending an `Approved` message.
Before using it remove `_example` from the filename:

Specify users in `users.json` in the following format:
```json
{
    "Trello Name": 141382000521798975
}
```

## Running the Bot
After installing all dependencies and configuring the files, run the bot with:

```bash
py main.py
```

