import json
import os
from app.utils.logger import log_to_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)
USERS_JSON_PATH = os.path.join(APP_DIR, "resources", "users.json")

def load_user_ids():
    try:
        with open(USERS_JSON_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        log_to_file(
            f"users.json not found at {USERS_JSON_PATH}. Mentions disabled.",
            level="WARN",
            component="users_loader",
        )
    except json.JSONDecodeError as exc:
        log_to_file(
            f"users.json has invalid JSON: {exc}. Mentions disabled.",
            level="ERROR",
            component="users_loader",
        )
    except OSError as exc:
        log_to_file(
            f"Failed to read users.json: {exc}. Mentions disabled.",
            level="ERROR",
            component="users_loader",
        )
    return {}
