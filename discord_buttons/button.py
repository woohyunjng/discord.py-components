from discord import InvalidArgument, Emoji

from typing import Union, Optional
from uuid import uuid1
from random import randint


__all__ = ("ButtonStyle", "Button")


class ButtonStyle:
    """A class containing button styles"""

    blue = 1
    gray = 2
    grey = 2
    green = 3
    red = 4
    URL = 5

    @classmethod
    def randomColor(cls) -> int:
        """Returns a random number between 1, 5

        :returns: :class:`int`
        """

        return randint(1, cls.red)

    @classmethod
    def to_dict(cls) -> dict:
        """Returns a dict containing style information

        :returns: :class:`dict`
        """

        return {
            "blue": cls.blue,
            "gray": cls.gray,
            "green": cls.green,
            "red": cls.red,
            "URL": cls.URL,
        }


class Button:
    """The button class

    Parameters
    ----------
    label: :class:`str`
        The bot's label
    style: :class:`style`
        The bot's style (1 or more and 5 or less)
    id: :class:`str`
        The button's id.

        If this was not passed as an argument when initailized, this value is random
    url: :class:`str`
        The button's hyperlink.
    disabled: :class:`bool`
        bool: If the buttons is disabled
    emoji: Union[:class:`discord.Emoji`, :class:`str`]
        The button's emoji
    """

    __slots__ = ("_style", "_label", "_id", "_url", "_disabled", "_emoji")

    def __init__(
        self,
        *,
        label: str,
        style: int = ButtonStyle.gray,
        id: Optional[str] = None,
        url: Optional[str] = None,
        disabled: bool = False,
        emoji: Emoji = None,
    ):
        if style == ButtonStyle.URL and not url:
            raise InvalidArgument("You must provide a URL when the style is URL")
        if style == ButtonStyle.URL and id:
            raise InvalidArgument("You musn't use both id and url")
        if not (1 <= style <= ButtonStyle.URL):
            raise InvalidArgument(f"style must be in between 1, {ButtonStyle.URL}")

        if not len(label):
            raise InvalidArgument("Label musn't be empty")

        self._style = style
        self._label = label
        self._url = url
        self._disabled = disabled
        self._emoji = emoji

        if not self.style == ButtonStyle.URL:
            self._id = id or str(uuid1())
        else:
            self._id = None

    def to_dict(self) -> dict:
        """
        Converts the button information required for API request to dict and returns

        :returns: :class:`dict`
        """

        data = {
            "type": 2,
            "style": self.style,
            "label": self.label,
            "custom_id": self.id,
            "url": self.url if self.style == ButtonStyle.URL else None,
            "disabled": self.disabled,
        }
        if self.emoji:
            emojidata = {}
            if isinstance(self.emoji, str):
                emojidata["name"] = self.emoji
            elif isinstance(self.emoji, Emoji):
                emojidata = {"id": self.emoji.id, "name": self.emoji.name}
                if self.emoji.animated:
                    emojidata["animated"] = True
            data["emoji"] = emojidata

        return data

    @property
    def style(self) -> int:
        """:class:`int`: The button's style (1 or more and 5 or less)"""
        return self._style

    @property
    def label(self) -> str:
        """:class:`str`: The button's label"""
        return self._label

    @property
    def id(self) -> str:
        """:class:`str`: The button's id."""
        return self._id

    @property
    def url(self) -> Optional[str]:
        """Optional[:class:`str`]: The button's hyperlink.

        .. note::
            If the button's style is not `5`(URL), this value is `None`
        """
        return self._url

    @property
    def disabled(self) -> bool:
        """Optional[:class:`str`]: If the buttons is disabled"""
        return self._disabled

    @property
    def emoji(self) -> Union[Emoji, str]:
        """Union[:class:`discord.Emoji`, :class:`str`]: The button's emoji"""
        return self._emoji

    @label.setter
    def label(self, value: str):
        if not len(value):
            raise InvalidArgument("Label musn't be empty")

        self._label = value

    @url.setter
    def url(self, value: str):
        if self.style != ButtonStyle.URL:
            raise InvalidArgument("button style is not URL")

        self._url = value

    @id.setter
    def id(self, value: str):
        if self.style == ButtonStyle.URL:
            raise InvalidArgument("button style is URL")

        self._id = id

    @disabled.setter
    def disabled(self, value: bool):
        self._disabled = value

    @emoji.setter
    def emoji(self, value: bool):
        self._emoji = value

    def __repr__(self) -> str:
        id_st = f"id='{self.id}'" if self.id else ""
        url_st = f"url='{self.url}'" if self.url else ""
        return f"<Button style={self.style} label='{self.label}' {url_st} {id_st}>"

    def __str__(self) -> str:
        return self.__repr__()
