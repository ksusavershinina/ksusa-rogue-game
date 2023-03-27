from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseComponent:
    """BaseComponent is a base class in the game that defines the common properties
    and behaviors for various components in the game, such as Fighter, Inventory, Level, and Equipment"""
    parent: Entity  # Экземпляр сущности-владельца.
    # property - позволяет объявить атрибут(поле) в классе как атрибут-свойство
    # то есть к нему можно обращаться и как к полю, и как к атрибуту
    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap
    @property
    def engine(self) -> Engine:
        return self.gamemap.engine