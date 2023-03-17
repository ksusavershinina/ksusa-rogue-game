#!/usr/bin/env python3
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:
    # screen size
    screen_width = 80
    screen_height = 50

    player_x = int (screen_width / 2)
    player_y = int (screen_height / 2)

    # Return a new Tileset from a simple tilesheet image.
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD # для подгружения символов по правилам tcod, а не стандратным
    )
    # объект EventHandler
    event_handler = EventHandler()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="My First Roguelike Game",
        vsync=True, # синхронизация кадровой частоты с частотой монитора
    # типа место для генерации игры. аналогично понятию консоли
    ) as context:
        # order задает порядок отображения Ох и Оу
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")
            # рисует консоль
            context.present(root_console)
            # ждет нажатия/клика от юзера
            root_console.clear()
            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()