from discord import InvalidArgument, PartialEmoji, Emoji

from typing import List
from uuid import uuid1

from .component import Component


__all__ = ("Select", "Option")


class Option(Component):
    """The select option.

    Parameters
    ----------
    label: :class:`str`
        The option's label.
    value: :class:`str`
        The option's value.
    emoji: :class:`discord.PartialEmoji`
        The option's emoji.
    description: :class:`str`
        The option's description.
    default: :class:`bool`
        Indicates if the option is default.
    """

    __slots__ = ("_label", "_value", "_emoji", "_description", "_default")

    def __init__(
        self,
        *,
        label,
        value,
        emoji=None,
        description=None,
        default=False,
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
        """
        Converts the select option information required for API request to dict and returns.

        :returns: :class:`dict`
        """

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
        """:class:`str`: The option's label."""
        return self._label

    @property
    def value(self) -> str:
        """:class:`str`: The option's value."""
        return self._value

    @property
    def emoji(self) -> PartialEmoji:
        """:class:`discord.PartialEmoji`: The option's emoji."""
        return self._emoji

    @property
    def description(self) -> str:
        """:class:`str`: The option's description."""
        return self._description

    @property
    def default(self) -> bool:
        """:class:`bool`: Indicates if the option is default."""
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
    def emoji(self, emoji: PartialEmoji):
        if isinstance(emoji, PartialEmoji):
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
    def from_json(data):
        """Creates option instance from json.

        :returns: :class:`~discord_components.Option`

        Parameters
        ----------
        data: :class:`dict`
            The json to construct option from.
        """

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
    """The select.

    Parameters
    ----------
    options: List[:class:`~discord_components.Option`]
        The select's options.
    id: :class:`str`
        The select's id.
    placeholder: :class:`str`
        The select's placeholder.
    min_values: :class:`int`
        The select's min values.
    max_values: :class:`int`
        The select's max values.
    """

    __slots__ = ("_id", "_options", "_placeholder", "_min_values", "_max_values")

    def __init__(
        self,
        *,
        options,
        id=None,
        placeholder=None,
        min_values=None,
        max_values=None,
    ):
        if (not len(options)) or (len(options) > 25):
            raise InvalidArgument("Options length should be between 1 and 25.")

        self._id = id or str(uuid1())
        self._options = options
        self._placeholder = placeholder
        self._min_values = min_values
        self._max_values = max_values

    def to_dict(self) -> dict:
        """
        Converts the select information required for API request to dict and returns.

        :returns: :class:`dict`
        """

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
        """:class:`str`: The select's id."""
        return self._id

    @property
    def options(self) -> List[Option]:
        """List[:class:`~discord_components.Option`]: The select's options."""
        return self._options

    @property
    def placeholder(self) -> str:
        """:class:`str`: The select's placeholder."""
        return self._placeholder

    @property
    def min_values(self) -> int:
        """:class:`int`: The select's min values."""
        return self._min_values

    @property
    def max_values(self) -> int:
        """:class:`int`: The select's max values."""
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
    def from_json(data):
        """Creates a select instance from json.

        :returns: :class:`~discord_components.Select`

        Parameters
        ----------
        data: :class:`dict`
            The json to construct select from.
        """

        return Select(
            id=data["custom_id"],
            options=list(map(lambda x: Option.from_json(x), data["options"])),
            placeholder=data.get("placeholder"),
            min_values=data.get("min_values"),
            max_values=data.get("max_values"),
        )
