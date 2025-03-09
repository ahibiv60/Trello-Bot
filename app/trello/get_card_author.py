import time
import requests
from app.utils.logger import log_to_file
from app.config.config import TRELLO_KEY, TRELLO_TOKEN, MAX_ATTEMPTS

def get_card_author(card_id):
    url = f"https://api.trello.com/1/cards/{card_id}/actions"
    params = {'filter': 'createCard', 'key': TRELLO_KEY, 'token': TRELLO_TOKEN}

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                actions = response.json()
                if actions and 'memberCreator' in actions[0]:
                    return actions[0]['memberCreator'].get('fullName', "Unknown")
            elif response.status_code == 429:
                log_to_file(f"Trello API limit exceeded while retrieving author. Waiting 30 seconds... (Try {attempt}/{MAX_ATTEMPTS})")
                time.sleep(30)
            else:
                log_to_file(f"Error retrieving card author ({response.status_code}): {response.text}")
                return "Unknown"
        except requests.exceptions.RequestException as e:
            log_to_file(f"Network problem: {e}. Waiting 10 minutes... (Try {attempt}/{MAX_ATTEMPTS})")
            time.sleep(600)

    log_to_file("Failed to retrieve author after 5 attempts")
    return "Unknown"