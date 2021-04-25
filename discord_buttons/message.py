from discord import Message

from typing import List

from .button import Button


class ButtonMessage(Message):
    """A message with buttons

    Parameters
    ----------
    buttons: List[:class:`discord_buttons.Button`]
        The message's buttons

    Attributes
    ----------
    buttons: List[:class:`discord_buttons.Button`]
        The message's buttons
    """

    def __init__(self, *, buttons: List[Button], **kwargs):
        super().__init__(**kwargs)
        self.buttons = buttons
