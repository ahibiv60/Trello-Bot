import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)
USERS_JSON_PATH = os.path.join(APP_DIR, "resources", "users.json")

def load_user_ids():
    with open(USERS_JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)