# Trello Bot

Trello Bot sends notifications to Discord when cards appear in selected Trello lists.

## Features
- Polls Trello lists via API.
- Sends messages to Discord via webhook.
- Mentions mapped users for `approved` events.

## Requirements
- Python 3.13.x (recommended)
- pip

## Installation
1. Clone repository.
2. Open project folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### 1) `config.env`
Create `config.env` from `config_example.env` and fill values:
- `ENVIRONMENT` must be `main` or `test`.
- `TRELLO_KEY`
- `TRELLO_TOKEN`
- `READY_LIST_ID`
- `APPROVED_LIST_ID`
- `DISCORD_WEBHOOK_URL_MAIN`
- `DISCORD_WEBHOOK_URL_TEST`

### 2) `app/resources/users.json`
Create `app/resources/users.json` from `app/resources/users_example.json`.
This file maps Trello full names to Discord user IDs:

```json
{
  "Trello Name": 141382000521798975
}
```

If the file is missing or invalid, bot still works, but sends messages without mentions.

## Run

```bash
py main.py
```
