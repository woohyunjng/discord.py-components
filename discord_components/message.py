from discord import Message
from typing import List, Union

from .component import Component


class ComponentMessage(Message):
    """A message with components.

    Parameters
    ----------
    components: List[Union[:class:`~discord_components.Component`, List[:class:`~discord_components.Component`]]]
        The message's components.

    Attributes
    ----------
    components: List[Union[:class:`~discord_components.Component`, List[:class:`~discord_components.Component`]]]
        The message's components.
    """

    def __init__(self, *, components=[], **kwargs):
        super().__init__(**kwargs)
        self.components = components
