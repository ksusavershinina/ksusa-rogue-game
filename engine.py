# рисует карты и объекты
from __future__ import annotations
from typing import TYPE_CHECKING
import lzma # provides classes and convenience functions for compressing and decompressing data
import pickle # для сериализации и десериализации объектов Python. (в байты и назад)
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld
class Engine:
    """рисует карты и объекты"""
# entitles - набор сущностей, которые будут генериться
# event_handler -  handle our events
# player - удобно передать отдельно, потому что мы с ним будем много взаимодействовать
# определяют два атрибута класса - переменная, определенная на уровне класса, а не на уровне экземпляра
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        """позволяет неписям двигаться и дамажить. если у нее есть интеллект, то мы вызываем perform"""
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.
    def update_fov(self) -> None:
        """Пересчитывает видимую зону с точки зрения игрока"""
        self.game_map.visible[:] = compute_fov(
            # массив для просчитывания поля зрения
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # если плиточка видимая, то ее стоит добавить в открытые
        # эта строчка добавляет только что открытые плитки в массив уже увиденных
        # операция - побитовое присваивание - +- добавление подмножества в множество
        self.game_map.explored |= self.game_map.visible

    # контекст позволяет делать более крутой вывод
    def render(self, console: Console) -> None:
        """рисует весь экран со всеми включениями (хп, сообщения, пещеры)"""
        self.game_map.render(console)

        self.message_log.render(
            console=console,
            x=22,
            y=42,
            width=60,
            height=8
        )

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        render_functions.render_names_at_mouse_location(
            console=console, x=0, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        # pickle.dumps serializes an object hierarchy in Python.
        # lzma.compress compresses the data,
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f: # to write the file
            f.write(save_data)
