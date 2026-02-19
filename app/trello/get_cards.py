import time
import requests
from app.utils.logger import log_to_file
from app.config.config import TRELLO_KEY, TRELLO_TOKEN, MAX_ATTEMPTS

def get_cards_in_list(list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "fields": "name,shortUrl,idMembers",
        "members": "true",
        "member_fields": "fullName",
    }

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                cards = {}
                for card in response.json():
                    member_names = [
                        member.get("fullName")
                        for member in card.get("members", [])
                        if member.get("fullName")
                    ]
                    cards[card["id"]] = {
                        "name": card["name"],
                        "url": card["shortUrl"],
                        "member_names": member_names,
                    }
                return cards
            elif response.status_code == 429:
                log_to_file(
                    f"Rate limit hit for list_id={list_id}. Retry in 30s "
                    f"(attempt {attempt}/{MAX_ATTEMPTS}).",
                    level="WARN",
                    component="trello.cards",
                )
                time.sleep(30)
            else:
                log_to_file(
                    f"Request failed for list_id={list_id}. "
                    f"status={response.status_code}, body={response.text}",
                    level="ERROR",
                    component="trello.cards",
                )
                return None
        except requests.exceptions.RequestException as e:
            backoff_seconds = min(30, 2 ** attempt)
            log_to_file(
                f"Network error for list_id={list_id}: {e}. Retry in {backoff_seconds}s "
                f"(attempt {attempt}/{MAX_ATTEMPTS}).",
                level="WARN",
                component="trello.cards",
            )
            time.sleep(backoff_seconds)

    log_to_file(
        f"Failed to fetch cards for list_id={list_id} after {MAX_ATTEMPTS} attempts.",
        level="ERROR",
        component="trello.cards",
    )
    return None
