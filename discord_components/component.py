from discord import PartialEmoji, Emoji
from typing import Union

__all__ = ("Component",)


def get_partial_emoji(emoji: Union[Emoji, PartialEmoji, str]) -> PartialEmoji:
    if isinstance(emoji, Emoji):
        return PartialEmoji(name=emoji.name, animated=emoji.animated, id=emoji.id)
    elif isinstance(emoji, PartialEmoji):
        return emoji
    elif isinstance(emoji, str):
        return PartialEmoji(name=emoji)


class Component:
    def to_dict(self) -> dict:
        raise NotImplementedError()

    def from_dict(self, data: dict):
        raise NotImplementedError()
