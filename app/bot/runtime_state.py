from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Set

from app.utils.logger import log_to_console


@dataclass
class RuntimeState:
    sent_ready_cards: Set[str] = field(default_factory=set)
    sent_approved_cards: Set[str] = field(default_factory=set)
    trello_cooldown_seconds: int = 600
    discord_cooldown_seconds: int = 600
    trello_cooldown_until: Optional[datetime] = None
    discord_cooldown_until: Optional[datetime] = None

    @staticmethod
    def _is_cooldown_active(cooldown_until: Optional[datetime]) -> bool:
        return cooldown_until is not None and datetime.now() < cooldown_until

    def is_trello_cooldown_active(self) -> bool:
        return self._is_cooldown_active(self.trello_cooldown_until)

    def is_discord_cooldown_active(self) -> bool:
        return self._is_cooldown_active(self.discord_cooldown_until)

    def set_trello_cooldown(self) -> None:
        if self.is_trello_cooldown_active():
            return

        self.trello_cooldown_until = datetime.now() + timedelta(
            seconds=self.trello_cooldown_seconds
        )
        log_to_console(
            f"Trello cooldown started for {self.trello_cooldown_seconds} seconds.",
            level="WARN",
            component="cooldown.trello",
        )

    def set_discord_cooldown(self) -> None:
        if self.is_discord_cooldown_active():
            return

        self.discord_cooldown_until = datetime.now() + timedelta(
            seconds=self.discord_cooldown_seconds
        )
        log_to_console(
            f"Discord cooldown started for {self.discord_cooldown_seconds} seconds.",
            level="WARN",
            component="cooldown.discord",
        )
