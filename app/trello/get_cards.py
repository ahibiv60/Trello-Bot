import time
import requests
from app.utils.logger import log_to_file
from app.config.config import TRELLO_KEY, TRELLO_TOKEN, MAX_ATTEMPTS

def get_cards_in_list(list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    params = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return {card['id']: {'name': card['name'], 'url': card['shortUrl']} for card in response.json()}
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
            log_to_file(
                f"Network error for list_id={list_id}: {e}. Retry in 600s "
                f"(attempt {attempt}/{MAX_ATTEMPTS}).",
                level="WARN",
                component="trello.cards",
            )
            time.sleep(600)

    log_to_file(
        f"Failed to fetch cards for list_id={list_id} after {MAX_ATTEMPTS} attempts.",
        level="ERROR",
        component="trello.cards",
    )
    return None
