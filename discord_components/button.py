from discord import InvalidArgument, PartialEmoji, Emoji

from typing import Optional, Union
from uuid import uuid1
from random import randint

from .component import Component


__all__ = ("ButtonStyle", "Button")


class ButtonStyle:
    blue: int = 1
    gray: int = 2
    grey: int = 2
    green: int = 3
    red: int = 4
    URL: int = 5

    @classmethod
    def random_color(cls) -> int:
        return randint(1, cls.red)

    @classmethod
    def to_dict(cls) -> dict:
        return {
            "blue": cls.blue,
            "gray": cls.gray,
            "green": cls.green,
            "red": cls.red,
            "URL": cls.URL,
        }


class Button(Component):
    __slots__ = ("_style", "_label", "_id", "_url", "_disabled", "_emoji")

    def __init__(
        self,
        *,
        label: str = None,
        style: int = ButtonStyle.gray,
        id: str = None,
        url: str = None,
        disabled: bool = False,
        emoji: Union[Emoji, PartialEmoji, str] = None,
    ):
        if style == ButtonStyle.URL and not url:
            raise InvalidArgument("You must provide a URL when the style is set to URL.")
        if style == ButtonStyle.URL and id:
            raise InvalidArgument("Both ID and URL are set.")
        if not (1 <= style <= ButtonStyle.URL):
            raise InvalidArgument(f"Style must be between 1, {ButtonStyle.URL}.")

        if not label and not emoji:
            raise InvalidArgument(f"Label or emoji must be given.")

        self._style = style
        self._label = label
        self._url = url
        self._disabled = disabled

        if isinstance(emoji, Emoji):
            self._emoji = PartialEmoji(name=emoji.name, animated=emoji.animated, id=emoji.id)
        elif isinstance(emoji, PartialEmoji):
            self._emoji = emoji
        elif isinstance(emoji, str):
            self._emoji = PartialEmoji(name=emoji)
        else:
            self._emoji = None

        if not self.style == ButtonStyle.URL:
            self._id = id or str(uuid1())
        else:
            self._id = None

    def to_dict(self) -> dict:
        data = {
            "type": 2,
            "style": self.style,
            "label": self.label,
            "custom_id": self.id,
            "url": self.url if self.style == ButtonStyle.URL else None,
            "disabled": self.disabled,
        }
        if self.emoji:
            data["emoji"] = self.emoji.to_dict()
        return data

    @property
    def style(self) -> int:
        return self._style

    @property
    def label(self) -> str:
        return self._label

    @property
    def id(self) -> str:
        return self._id

    @property
    def url(self) -> Optional[str]:
        return self._url

    @property
    def disabled(self) -> bool:
        return self._disabled

    @property
    def emoji(self) -> PartialEmoji:
        return self._emoji

    @style.setter
    def style(self, value: int):
        if value == ButtonStyle.URL and self.id:
            raise InvalidArgument("Both ID and URL are set.")
        if not (1 <= value <= ButtonStyle.URL):
            raise InvalidArgument(f"Style must be between 1, {ButtonStyle.URL}.")

        self._style = value

    @label.setter
    def label(self, value: str):
        if not value and not self.emoji:
            raise InvalidArgument("Label should not be empty.")

        self._label = value

    @url.setter
    def url(self, value: str):
        if value and self.style != ButtonStyle.URL:
            raise InvalidArgument("Button style is not URL. You shouldn't provide URL.")

        self._url = value

    @id.setter
    def id(self, value: str):
        if self.style == ButtonStyle.URL:
            raise InvalidArgument("Button style is set to URL. You shouldn't provide ID.")

        self._id = value

    @disabled.setter
    def disabled(self, value: bool):
        self._disabled = value

    @emoji.setter
    def emoji(self, emoji: Union[Emoji, PartialEmoji, str]):
        if isinstance(emoji, Emoji):
            self._emoji = PartialEmoji(name=emoji.name, animated=emoji.animated, id=emoji.id)
        elif isinstance(emoji, PartialEmoji):
            self._emoji = emoji
        elif isinstance(emoji, str):
            self._emoji = PartialEmoji(name=emoji)

    @staticmethod
    def from_json(data: dict):
        emoji = data.get("emoji")
        return Button(
            style=data["style"],
            label=data.get("label"),
            id=data.get("custom_id"),
            url=data.get("url"),
            disabled=data.get("disabled", False),
            emoji=PartialEmoji(
                name=emoji["name"], animated=emoji.get("animated", False), id=emoji.get("id")
            )
            if emoji
            else None,
        )
