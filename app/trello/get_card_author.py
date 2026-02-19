import time
import requests
from app.utils.logger import log_to_file
from app.config.config import TRELLO_KEY, TRELLO_TOKEN, MAX_ATTEMPTS

def get_card_author(card_id):
    url = f"https://api.trello.com/1/cards/{card_id}/actions"
    params = {'filter': 'copyCard,createCard', 'key': TRELLO_KEY, 'token': TRELLO_TOKEN}

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                actions = response.json()
                if actions and 'memberCreator' in actions[0]:
                    return actions[0]['memberCreator'].get('fullName', "Unknown")
                log_to_file(
                    f"No creator action found for card_id={card_id}. Using 'Unknown'.",
                    level="WARN",
                    component="trello.author",
                )
                return "Unknown"
            elif response.status_code == 429:
                log_to_file(
                    f"Rate limit hit while reading author for card_id={card_id}. Retry in 30s "
                    f"(attempt {attempt}/{MAX_ATTEMPTS}).",
                    level="WARN",
                    component="trello.author",
                )
                time.sleep(30)
            else:
                log_to_file(
                    f"Failed to read author for card_id={card_id}. "
                    f"status={response.status_code}, body={response.text}",
                    level="ERROR",
                    component="trello.author",
                )
                return "Unknown"
        except requests.exceptions.RequestException as e:
            log_to_file(
                f"Network error while reading author for card_id={card_id}: {e}. Retry in 600s "
                f"(attempt {attempt}/{MAX_ATTEMPTS}).",
                level="WARN",
                component="trello.author",
            )
            time.sleep(600)

    log_to_file(
        f"Failed to read author for card_id={card_id} after {MAX_ATTEMPTS} attempts.",
        level="ERROR",
        component="trello.author",
    )
    return "Unknown"
