from typing import Dict, Set

from app.bot.runtime_state import RuntimeState
from app.discord.send_to_discord import send_to_discord
from app.trello.get_card_author import get_card_author
from app.trello.get_cards import get_cards_in_list
from app.utils.logger import log_to_console


def resolve_card_author(card_id: str, card_data: Dict[str, object]) -> str:
    member_names = card_data.get("member_names", [])
    if member_names:
        return member_names[0]
    return get_card_author(card_id)


def process_cards_in_list(
    list_id: str,
    list_name: str,
    sent_cards: Set[str],
    environment: str,
    state_component: str,
    log_component: str,
    state: RuntimeState,
) -> bool:
    current_cards = get_cards_in_list(list_id)
    if current_cards is None:
        log_to_console(
            f"Failed to fetch list cards for {list_name} list (list_id={list_id}). "
            f"Cycle skipped.",
            level="WARN",
            component=log_component,
        )
        state.set_trello_cooldown()
        return False

    new_cards = {
        card_id: data
        for card_id, data in current_cards.items()
        if card_id not in sent_cards
    }
    removed_cards = sent_cards - set(current_cards.keys())

    for card_id, card_data in new_cards.items():
        if state.is_discord_cooldown_active():
            return True

        author = resolve_card_author(card_id, card_data)
        send_status = send_to_discord(author, card_data["name"], card_data["url"], list_name)

        if send_status == "sent":
            sent_cards.add(card_id)
        elif send_status == "retryable_failure":
            state.set_discord_cooldown()
            return True
        else:
            sent_cards.add(card_id)

    if removed_cards:
        sent_cards -= removed_cards

    if environment == "test":
        log_to_console(
            f"Cached {list_name} card ids: {sorted(sent_cards)}",
            component=state_component,
        )

    return True
