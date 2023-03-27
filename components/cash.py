from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class Cash(BaseComponent):
    parent: Actor

    def __init__(
        self,
        current_cash: int = 0,
        money_given: int = 0,
    ):
        self.current_cash = current_cash
        self.money_given = money_given

    def add_cash(self, coins: int) -> None:
        if coins == 0:
            return

        self.current_cash += coins

        self.engine.message_log.add_message(f"You gain {coins} coin(s)")

    def lose_cash(self, coins: int):
        self.current_cash -= coins