from discord import Message
from typing import List

from .button import Button


class ComponentMessage(Message):
    """A message with components

    Parameters
    ----------
    buttons: List[:class:`~discord_components.Button`]
        The message's buttons

    Attributes
    ----------
    buttons: List[:class:`~discord_components.Button`]
        The message's buttons
    """

    def __init__(self, *, buttons: List[Button], **kwargs):
        super().__init__(**kwargs)
        self.buttons = buttons
