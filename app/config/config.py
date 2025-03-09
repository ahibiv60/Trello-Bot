import os
from dotenv import load_dotenv

MAX_ATTEMPTS = 5

load_dotenv("config.env")

ENVIRONMENT = os.getenv("ENVIRONMENT")
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
READY_LIST_ID = os.getenv("READY_LIST_ID")
APPROVED_LIST_ID = os.getenv("APPROVED_LIST_ID")

if ENVIRONMENT == "main":
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL_MAIN")
    requests_frequency = 20
    scheduler = True
else:
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL_TEST")
    requests_frequency = 5
    scheduler = False