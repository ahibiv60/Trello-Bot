import time

import requests

from app.config.config import DISCORD_WEBHOOK_URL, MAX_ATTEMPTS
from app.utils.logger import log_to_file
from app.utils.users_loader import load_user_ids

USER_IDS = load_user_ids()


def process_message(author, card_name, card_url, list_name):
    if list_name == "ready":
        embed = {
            "title": ":pencil: Created new card in Trello",
            "description": f"Author: {author}\n{card_name}",
            "color": 3447003,
            "fields": [
                {
                    "name": ":link: Link to card",
                    "value": f"[View]({card_url})",
                    "inline": False,
                }
            ],
        }
        return {"embeds": [embed]}

    if list_name == "approved":
        user_id = USER_IDS.get(author)
        mention = f"<@{user_id}>" if user_id else author

        embed = {
            "title": ":white_check_mark: Card approved!",
            "description": f"{card_name}",
            "color": 65280,
            "fields": [
                {
                    "name": ":link: Link to card",
                    "value": f"[View]({card_url})",
                    "inline": False,
                }
            ],
        }

        return {
            "content": mention,
            "embeds": [embed],
        }

    return None


def send_to_discord(author, card_name, card_url, list_name):
    data = process_message(author, card_name, card_url, list_name)
    if data is None:
        log_to_file(
            f"Unsupported list type='{list_name}'. Message skipped for card_url={card_url}.",
            level="ERROR",
            component="discord.send",
        )
        return "hard_failure"

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
            if response.status_code in [200, 204]:
                log_to_file(
                    f"Sent message for list='{list_name}', author='{author}', card_url={card_url}.",
                    component="discord.send",
                )
                return "sent"
            if response.status_code == 429:
                retry_after = max(1, int(float(response.headers.get("Retry-After", 30))))
                log_to_file(
                    f"Rate limit hit. Retry in {retry_after}s "
                    f"(attempt {attempt}/{MAX_ATTEMPTS}) for card_url={card_url}.",
                    level="WARN",
                    component="discord.send",
                )
                time.sleep(retry_after)
                continue

            log_to_file(
                f"Failed to send message. status={response.status_code}, "
                f"body={response.text}, card_url={card_url}.",
                level="ERROR",
                component="discord.send",
            )
            return "hard_failure"
        except requests.exceptions.RequestException as exc:
            backoff_seconds = min(30, 2 ** attempt)
            log_to_file(
                f"Network error while sending card_url={card_url}: {exc}. "
                f"Retry in {backoff_seconds}s (attempt {attempt}/{MAX_ATTEMPTS}).",
                level="WARN",
                component="discord.send",
            )
            time.sleep(backoff_seconds)

    log_to_file(
        f"Failed to send card_url={card_url} after {MAX_ATTEMPTS} attempts.",
        level="ERROR",
        component="discord.send",
    )
    return "retryable_failure"
