import time

from app.bot.processor import process_cards_in_list
from app.bot.runtime_state import RuntimeState
from app.config.config import (
    APPROVED_LIST_ID,
    DISCORD_WEBHOOK_URL,
    ENVIRONMENT,
    READY_LIST_ID,
    TRELLO_KEY,
    TRELLO_TOKEN,
    requests_frequency,
    scheduler,
)
from app.utils.logger import log_to_console
from app.utils.scheduler import wait_until_working_hours


def validate_configuration() -> None:
    if ENVIRONMENT not in {"main", "test"}:
        raise ValueError("Invalid ENVIRONMENT value. Use 'main' or 'test' in config.env.")

    required_values = [
        ENVIRONMENT,
        TRELLO_KEY,
        TRELLO_TOKEN,
        READY_LIST_ID,
        APPROVED_LIST_ID,
        DISCORD_WEBHOOK_URL,
    ]
    if not all(required_values):
        raise ValueError("Not all config values are loaded. Check config.env")


def run_bot() -> None:
    log_to_console("Application started", component="bootstrap")
    log_to_console(f"Environment={ENVIRONMENT}", component="bootstrap")

    validate_configuration()
    runtime_state = RuntimeState()

    try:
        while True:
            if scheduler:
                wait_until_working_hours()

            if runtime_state.is_trello_cooldown_active():
                time.sleep(requests_frequency)
                continue

            process_cards_in_list(
                list_id=READY_LIST_ID,
                list_name="ready",
                sent_cards=runtime_state.sent_ready_cards,
                environment=ENVIRONMENT,
                state_component="state.ready",
                log_component="trello.ready",
                state=runtime_state,
            )
            process_cards_in_list(
                list_id=APPROVED_LIST_ID,
                list_name="approved",
                sent_cards=runtime_state.sent_approved_cards,
                environment=ENVIRONMENT,
                state_component="state.approved",
                log_component="trello.approved",
                state=runtime_state,
            )

            time.sleep(requests_frequency)
    except KeyboardInterrupt:
        log_to_console("Application stopped by user", level="WARN", component="bootstrap")
