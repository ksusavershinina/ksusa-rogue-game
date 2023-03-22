# отвечает за отображение всех сообщений не в терминал, а в контекст игры
from typing import Iterable, List, Reversible, Tuple
import textwrap

import tcod

import color


class Message:
    """используется для сохранения текста и цвета сообщений в логе
    + для подсчета количества"""
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text # актуальное сообщение
        self.fg = fg # цвет сообщения
        self.count = 1

    @property
    def full_text(self) -> str:
        """считает количество одинаковых сообщений, если их больше нуля"""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    """журнал сообщений, который позволяет добавлять новые сообщения и
    отображать их на экране"""
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
        self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True,
    ) -> None:
        """Add a message to this log.
        `text` is the message text, `fg` is the text color.
        If `stack(флаг)` is True then the message can stack with a previous message
        of the same text. Stack говорит нам, чтоит ли доавлять это сообщение в
         стек или нет.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1 # если предыдущее такое же, то просто увеличиваем счетчик
        else:
            self.messages.append(Message(text, fg)) # иначе добавляем в лист

    def render(
        self, console: tcod.Console, x: int, y: int, width: int, height: int,
    ) -> None:
        """Render this log over the given area.
        `x`, `y`, `width`, `height` is the rectangular region to render onto
        the `console`.
        """
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        """Return a wrapped text message."""
        for line in string.splitlines():  # Handle newlines in messages.
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )

    @classmethod
    def render_messages(
        cls,
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        """Render the messages provided.
        Сообщения ототбражаются, начиная с последнего и идут от последнего к первому.
        """
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # No more space to print messages.