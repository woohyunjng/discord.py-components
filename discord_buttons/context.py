from discord import User, Message, Client
from discord.ext.commands import Bot
from discord.http import Route

from .button import Button

from typing import Union


__all__ = "Context"


class Context:
    __slots__ = (
        "bot",
        "client",
        "user",
        "button",
        "raw_data",
        "message",
        "channel",
        "guild",
        "interaction_id",
        "interaction_token",
    )

    def __init__(
        self,
        *,
        bot: Union[Client, Bot],
        client: "DiscordButton",
        user: User,
        button: Button,
        raw_data: dict,
        message: Message,
    ):
        self.bot = bot
        self.client = client
        self.user = user

        self.button = button
        self.raw_data = raw_data

        self.message = message
        self.channel = message.channel
        self.guild = message.guild

        self.interaction_id = raw_data["d"]["id"]
        self.interaction_token = raw_data["d"]["token"]

    async def respond(self, *, type: int, data: dict = {}):
        await self.bot.http.request(
            Route("POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"),
            json={"type": type, "data": data},
        )
