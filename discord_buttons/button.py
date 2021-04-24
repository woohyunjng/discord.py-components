from typing import Union, Optional
from uuid import uuid1
from random import randint


__all__ = ("ButtonStyle", "Button")


class ButtonStyle:
    blue = 1
    gray = 2
    grey = 2
    green = 3
    red = 4
    URL = 5

    @classmethod
    def randomColor(cls) -> int:
        return randint(1, 4)

    @classmethod
    def to_dict(cls) -> dict:
        return {
            "blue": cls.blue,
            "gray": cls.gray,
            "green": cls.green,
            "red": cls.red,
            "URL": cls.URL,
        }


class Button:
    __slots__ = ("style", "label", "id", "url")

    def __init__(
        self, *, label: str, style: int = 1, id: Optional[str] = None, url: Optional[str] = None
    ):
        self.style = style
        self.label = label
        if url:
            self.id = None
        else:
            self.id = id or str(uuid1())
        self.url = url
