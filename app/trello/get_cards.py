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
                log_to_file(f"Trello API limit exceeded. Waiting 30 seconds... (Try {attempt}/{MAX_ATTEMPTS})")
                time.sleep(30)
            else:
                log_to_file(f"Error retrieving Trello cards ({response.status_code}): {response.text}")
                return {}
        except requests.exceptions.RequestException as e:
            log_to_file(f"Network problem: {e}. Waiting 10 minutes... (Try {attempt}/{MAX_ATTEMPTS})")
            time.sleep(600)

    log_to_file("Failed to retrieve data after 5 attempts")
    return {}