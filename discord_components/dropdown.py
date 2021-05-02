from discord import InvalidArgument

from typing import List
from uuid import uuid1

from .component import Component


__all__ = ("Dropdown", "Option")


class Option:
    """The dropdown option

    Parameters
    ----------
    label: :class:`str`
        The option's label
    value: :class:`str`
        The option's value
    """

    __slots__ = ("_label", "_value")

    def __init__(self, *, label: str, value: str):
        self._label = label
        self._value = value

    def to_dict(self) -> dict:
        """
        Converts the dropdown option information required for API request to dict and returns

        :returns: :class:`dict`
        """

        return {"label": self.label, "value": self.value}

    @property
    def label(self) -> str:
        """:class:`str`: The option's label"""
        return self._label

    @property
    def value(self) -> str:
        """:class:`str`: The option's value"""
        return self._value

    @label.setter
    def label(self, value: str):
        if not len(value):
            raise InvalidArgument("Label musn't be empty")

        self._label = value

    @value.setter
    def value(self, value: str):
        self._value = value

    def __repr__(self) -> str:
        return f"<Button label='{self.label}' value='{self.value}'"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def from_json(data: dict):
        """Create option instance from json

        :returns: :class:`~discord_components.Option`

        Parameters
        ----------
        data: :class:`dict`
            The json
        """

        return Option(label=data["label"], value=data["value"])


class Dropdown(Component):
    """The dropdown

    Parameters
    ----------
    options: List[:class:`~discord_components.Option`]
        The dropdown's options
    id: :class:`str`
        The dropdown's id
    """

    __slots__ = ("_id", "_options")

    def __init__(self, *, options: List[Option], id: str = None):
        if (not len(options)) or (len(options) > 25):
            raise InvalidArgument("options length should be between 1 and 25")

        self._id = id or str(uuid1())
        self._options = options

    def to_dict(self) -> dict:
        """
        Converts the dropdown information required for API request to dict and returns

        :returns: :class:`dict`
        """

        return {
            "options": list(map(lambda option: option.to_dict(), self.options)),
            "custom_id": self.id,
        }

    @property
    def id(self) -> str:
        """:class:`str`: The dropdown's id"""
        return self._id

    @property
    def options(self) -> List[Option]:
        """List[:class:`~discord_components.Option`]: The dropdown's options"""
        return self._options

    @id.setter
    def id(self, value: str):
        self._id = value

    @options.setter
    def options(self, value: List[Option]):
        if (not len(value)) or (len(value) > 25):
            raise InvalidArgument("options length should be between 1 and 25")

        self._options = value

    def __repr__(self) -> str:
        return f"<Button id='{self.id}' options=[{', '.join(map(lambda x: str(x), self.options))}]"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def from_json(data: dict):
        """Create dropdown instance from json

        :returns: :class:`~discord_components.Dropdown`

        Parameters
        ----------
        data: :class:`dict`
            The json
        """

        return Dropdown(
            id=data["custom_id"], options=list(map(lambda x: Option.from_json(x), data["options"]))
        )
