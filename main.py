import time
from app.config.config import (
    ENVIRONMENT,
    TRELLO_KEY,
    TRELLO_TOKEN,
    READY_LIST_ID,
    APPROVED_LIST_ID,
    DISCORD_WEBHOOK_URL,
    requests_frequency,
    scheduler,
)
from app.utils.logger import log_to_console
from app.utils.scheduler import wait_until_working_hours
from app.trello.get_cards import get_cards_in_list
from app.trello.get_card_author import get_card_author
from app.discord.send_to_discord import send_to_discord

sent_cards_in_ready_list = set()
sent_cards_in_approved_list = set()


def process_cards_in_ready_list():
    global sent_cards_in_ready_list

    current_cards = get_cards_in_list(READY_LIST_ID)
    if current_cards is None:
        log_to_console(
            f"Failed to fetch list cards for READY_LIST_ID={READY_LIST_ID}. Cycle skipped.",
            level="WARN",
            component="trello.ready",
        )
        return

    new_cards = {
        card_id: data
        for card_id, data in current_cards.items()
        if card_id not in sent_cards_in_ready_list
    }
    removed_cards = sent_cards_in_ready_list - set(current_cards.keys())

    for card_id, card_data in new_cards.items():
        author = get_card_author(card_id)
        send_to_discord(author, card_data["name"], card_data["url"], "ready")
        sent_cards_in_ready_list.add(card_id)

    if removed_cards:
        sent_cards_in_ready_list -= removed_cards

    if ENVIRONMENT == "test":
        log_to_console(
            f"Cached ready card ids: {sorted(sent_cards_in_ready_list)}",
            component="state.ready",
        )


def process_cards_in_approved_list():
    global sent_cards_in_approved_list

    current_cards = get_cards_in_list(APPROVED_LIST_ID)
    if current_cards is None:
        log_to_console(
            f"Failed to fetch list cards for APPROVED_LIST_ID={APPROVED_LIST_ID}. Cycle skipped.",
            level="WARN",
            component="trello.approved",
        )
        return

    new_cards = {
        card_id: data
        for card_id, data in current_cards.items()
        if card_id not in sent_cards_in_approved_list
    }
    removed_cards = sent_cards_in_approved_list - set(current_cards.keys())

    for card_id, card_data in new_cards.items():
        author = get_card_author(card_id)
        send_to_discord(author, card_data["name"], card_data["url"], "approved")
        sent_cards_in_approved_list.add(card_id)

    if removed_cards:
        sent_cards_in_approved_list -= removed_cards

    if ENVIRONMENT == "test":
        log_to_console(
            f"Cached approved card ids: {sorted(sent_cards_in_approved_list)}",
            component="state.approved",
        )


def main():
    log_to_console("Application started", component="bootstrap")
    log_to_console(f"Environment={ENVIRONMENT}", component="bootstrap")

    if ENVIRONMENT not in {"main", "test"}:
        raise ValueError("Invalid ENVIRONMENT value. Use 'main' or 'test' in config.env.")

    if not all(
        [
            ENVIRONMENT,
            TRELLO_KEY,
            TRELLO_TOKEN,
            READY_LIST_ID,
            APPROVED_LIST_ID,
            DISCORD_WEBHOOK_URL,
        ]
    ):
        raise ValueError("Not all config values are loaded. Check config.env")

    try:
        while True:
            if scheduler:
                wait_until_working_hours()
            process_cards_in_approved_list()
            process_cards_in_ready_list()
            time.sleep(requests_frequency)
    except KeyboardInterrupt:
        log_to_console("Application stopped by user", level="WARN", component="bootstrap")


if __name__ == "__main__":
    main()
