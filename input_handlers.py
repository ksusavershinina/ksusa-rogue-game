from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

# наследник EventDispatch - класс, который отправляет события в методы,
# которые зависят от типа передаваемого значения
class EventHandler(tcod.event.EventDispatch[Action]):
    # через -> написано, что возвращает. если optional,то модет вернуть None
    # это выход из игры
    # его мы переписали. по дефолту он чутка другой
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action