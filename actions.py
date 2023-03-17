class Action:
    pass

# наследники
class EscapeAction(Action):
    pass


class MovementAction(Action):
    # так принято передавать передавать аргументы по рер 484
    def __init__(self, dx: int, dy: int):
        # так как он наследник
        super().__init__()

        self.dx = dx
        self.dy = dy