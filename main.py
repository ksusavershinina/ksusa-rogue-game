#!/usr/bin/env python3
import tcod
import color
import traceback
import exceptions
import input_handlers
import setup_game


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main() -> None:
    # screen size
    screen_width = 82
    screen_height = 52

    # Return a new Tileset from a simple tilesheet image.
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD # для подгружения символов по правилам tcod, а не стандратным
    )

    # используется аннотация типов
    # input_handlers.BaseEventHandler - это аннотация типа, которая указывает, что переменная
    # handler должна быть экземпляром класса BaseEventHandler из модуля input_handlers.
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike Game",
        vsync=True, # Синхронизация кадровой частоты с частотой монитора
        # context - место для генерации игры. аналогично понятию консоли
    ) as context:
        # order задает порядок отображения Ох и Оу
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # gameloop
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise
if __name__ == "__main__":
    main()