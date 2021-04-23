from discord import User, Message
from .button import Button


class Context:
    def __init__(
        self, *, message: Message, user: User, button: Button, interaction_id: str, raw_data: dict
    ):
        self.message = message
        self.user = user
        self.button = button
        self.interaction_id = interaction_id
        self.raw_data = raw_data
        self.channel = message.channel
        self.guild = message.guild
        self.send = message.channel.send
