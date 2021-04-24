from discord import User, Message, Client
from discord.ext.commands import Bot
from discord.http import Route

from .button import Button

from typing import Union


class Context:
    def __init__(
        self,
        *,
        bot: Union[Client, Bot],
        client: "DiscordButton",
        message: Message,
        user: User,
        button: Button,
        interaction_id: str,
        raw_data: dict,
        interaction_token: str,
    ):
        self.bot = bot
        self.message = message
        self.user = user
        self.button = button
        self.interaction_id = interaction_id
        self.raw_data = raw_data
        self.channel = message.channel
        self.guild = message.guild
        self.interaction_token = interaction_token

    async def respond(self, *, type: int, data: dict = {}):
        await self.bot.http.request(
            Route("POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"),
            json={"type": type, "data": data},
        )
