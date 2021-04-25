from discord import Message

from typing import List

from .button import Button


class ButtonMessage(Message):
    def __init__(self, *, buttons: List[Button], **kwargs):
        super().__init__(**kwargs)
        self.buttons = buttons
