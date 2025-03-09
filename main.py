import time
from app.config.config import ENVIRONMENT, TRELLO_KEY, TRELLO_TOKEN, READY_LIST_ID, APPROVED_LIST_ID, DISCORD_WEBHOOK_URL, requests_frequency, scheduler
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
    new_cards = {card_id: data for card_id, data in current_cards.items() if card_id not in sent_cards_in_ready_list}
    removed_cards = sent_cards_in_ready_list - set(current_cards.keys())

    for card_id, card_data in new_cards.items():
        author = get_card_author(card_id)
        send_to_discord(author, card_data['name'], card_data['url'], "ready")
        sent_cards_in_ready_list.add(card_id)

    if removed_cards:
        sent_cards_in_ready_list -= removed_cards

    log_to_console("📌", f"Currently stored cards in ready collection: {sent_cards_in_ready_list}")

def process_cards_in_approved_list():
    global sent_cards_in_approved_list

    current_cards = get_cards_in_list(APPROVED_LIST_ID)
    new_cards = {card_id: data for card_id, data in current_cards.items() if card_id not in sent_cards_in_approved_list}
    removed_cards = sent_cards_in_approved_list - set(current_cards.keys())

    for card_id, card_data in new_cards.items():
        author = get_card_author(card_id)
        send_to_discord(author, card_data['name'], card_data['url'], "approved")
        sent_cards_in_approved_list.add(card_id)

    if removed_cards:
        sent_cards_in_approved_list -= removed_cards

    log_to_console("📌", f"Currently stored cards in approved collection: {sent_cards_in_approved_list}")

def main():
    log_to_console("🚀", "App started, checking Trello every 20 seconds...")
    print(f"Environment: {ENVIRONMENT}")
    
    if not all([TRELLO_KEY, TRELLO_TOKEN, READY_LIST_ID, DISCORD_WEBHOOK_URL]):
        raise ValueError("❌ Not all data loaded, check .env file")
    
    try:
        while True:
            if scheduler == True:
                wait_until_working_hours()
            process_cards_in_approved_list()
            process_cards_in_ready_list()
            time.sleep(requests_frequency)
    except KeyboardInterrupt:
        log_to_console("🛑", "App stopped")

if __name__ == "__main__":
    main()
