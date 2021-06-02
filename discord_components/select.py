from discord import InvalidArgument, PartialEmoji, Emoji

from typing import List, Union
from uuid import uuid1

from .component import Component


__all__ = ("Select", "Option")


class Option(Component):
    __slots__ = ("_label", "_value", "_emoji", "_description", "_default")

    def __init__(
        self,
        *,
        label: str,
        value: str,
        emoji: Union[Emoji, PartialEmoji, str] = None,
        description: str = None,
        default: bool = False,
    ):
        self._label = label
        self._value = value
        self._description = description
        self._default = default

        if isinstance(emoji, Emoji):
            self._emoji = PartialEmoji(name=emoji.name, animated=emoji.animated, id=emoji.id)
        elif isinstance(emoji, PartialEmoji):
            self._emoji = emoji
        elif isinstance(emoji, str):
            self._emoji = PartialEmoji(name=emoji)
        else:
            self._emoji = None

    def to_dict(self) -> dict:
        data = {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "default": self.default,
        }
        if self.emoji:
            data["emoji"] = self.emoji.to_dict()
        return data

    @property
    def label(self) -> str:
        return self._label

    @property
    def value(self) -> str:
        return self._value

    @property
    def emoji(self) -> PartialEmoji:
        return self._emoji

    @property
    def description(self) -> str:
        return self._description

    @property
    def default(self) -> bool:
        return self._default

    @label.setter
    def label(self, value: str):
        if not len(value):
            raise InvalidArgument("Label must not be empty.")

        self._label = value

    @value.setter
    def value(self, value: str):
        self._value = value

    @emoji.setter
    def emoji(self, emoji: Union[Emoji, PartialEmoji, str]):
        if isinstance(emoji, Emoji):
            self._emoji = PartialEmoji(name=emoji.name, animated=emoji.animated, id=emoji.id)
        elif isinstance(emoji, PartialEmoji):
            self._emoji = emoji
        elif isinstance(emoji, str):
            self._emoji = PartialEmoji(name=emoji)

    @description.setter
    def description(self, value: str):
        self._description = value

    @default.setter
    def default(self, value: bool):
        self._default = value

    @staticmethod
    def from_json(data: dict):
        emoji = data.get("emoji")
        return Option(
            label=data["label"],
            value=data["value"],
            emoji=PartialEmoji(
                name=emoji["name"], animated=emoji.get("animated", False), id=emoji.get("id")
            )
            if emoji
            else None,
            description=data.get("description"),
            default=data.get("default", False),
        )


class Select(Component):
    __slots__ = ("_id", "_options", "_placeholder", "_min_values", "_max_values")

    def __init__(
        self,
        *,
        options: List[Option],
        id: str = None,
        placeholder: str = None,
        min_values: int = None,
        max_values: int = None,
    ):
        if (not len(options)) or (len(options) > 25):
            raise InvalidArgument("Options length should be between 1 and 25.")

        self._id = id or str(uuid1())
        self._options = options
        self._placeholder = placeholder
        self._min_values = min_values
        self._max_values = max_values

    def to_dict(self) -> dict:
        return {
            "type": 3,
            "options": list(map(lambda option: option.to_dict(), self.options)),
            "custom_id": self.id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
        }

    @property
    def id(self) -> str:
        return self._id

    @property
    def options(self) -> List[Option]:
        return self._options

    @property
    def placeholder(self) -> str:
        return self._placeholder

    @property
    def min_values(self) -> int:
        return self._min_values

    @property
    def max_values(self) -> int:
        return self._max_values

    @id.setter
    def id(self, value: str):
        self._id = value

    @options.setter
    def options(self, value: List[Option]):
        if (not len(value)) or (len(value) > 25):
            raise InvalidArgument("Options length should be between 1 and 25.")

        self._options = value

    @placeholder.setter
    def placeholder(self, value: str):
        self._placeholder = value

    @min_values.setter
    def min_values(self, value: int):
        self._min_values = value

    @max_values.setter
    def max_values(self, value: int):
        self._max_values = value

    @staticmethod
    def from_json(data: dict):
        return Select(
            id=data["custom_id"],
            options=list(map(lambda x: Option.from_json(x), data["options"])),
            placeholder=data.get("placeholder"),
            min_values=data.get("min_values"),
            max_values=data.get("max_values"),
        )
