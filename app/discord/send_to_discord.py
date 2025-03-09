import time
import requests
from app.config.config import DISCORD_WEBHOOK_URL, MAX_ATTEMPTS
from app.utils.logger import log_to_file, log_to_console
from app.utils.users_loader import load_user_ids

USER_IDS = load_user_ids()

def check_author(author, card_name, card_url, list):
    if list == "ready":
            message = f"{author} added new card in Trello:\n**{card_name}**\n🔗 [Card link]({card_url})"
            return message
    elif list == "approved":
        USER_ID = USER_IDS.get(author)

        if USER_ID:
            return f"<@{USER_ID}> **your card approved**\n{card_name}\n🔗 [Card link]({card_url})"
        else:
            return f"{author} **your card approved**\n{card_name}\n🔗 [Card link]({card_url})"

def send_to_discord(author, card_name, card_url, list):
    message = check_author(author, card_name, card_url, list)
    data = {"content": message}

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
            if response.status_code in [200, 204]:
                log_to_file(f"Card {card_url} successfully sent to Discord")
                return
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 30))
                log_to_file(f"Discord has limited requests. Waiting {retry_after} seconds... (Try {attempt}/{MAX_ATTEMPTS})")
                time.sleep(retry_after)
            else:
                log_to_file(f"Error sending to Discord ({response.status_code}): {response.text}")
                return
        except requests.exceptions.RequestException as e:
            log_to_file(f"Network problem while sending to Discord: {e}. Waiting 10 minutes... (Try {attempt}/{MAX_ATTEMPTS})")
            time.sleep(600)

    log_to_file("Failed to send message to Discord after 5 attempts")