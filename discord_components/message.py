from discord import Message
from typing import List

from .button import Button
from .dropdown import Dropdown


class ComponentMessage(Message):
    """A message with components

    Parameters
    ----------
    buttons: List[:class:`~discord_components.Button`]
        The message's buttons
    dropdowns: List[:class:`~discord_components.Dropdown`]
        The message's dropdowns

    Attributes
    ----------
    buttons: List[:class:`~discord_components.Button`]
        The message's buttons
    dropdowns: List[:class:`~discord_components.Dropdown`]
        The message's dropdowns
    """

    def __init__(self, *, buttons: List[Button], dropdowns: List[Dropdown], **kwargs):
        super().__init__(**kwargs)
        self.buttons = buttons
        self.dropdowns = dropdowns
