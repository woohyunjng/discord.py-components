from discord import User, Message, Client, Embed, AllowedMentions
from discord.ext.commands import Bot
from discord.http import Route

from .button import Button

from typing import Union, List


__all__ = ("Context",)


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

    async def respond(
        self,
        *,
        type: int,
        content: str = None,
        embed: Embed = None,
        embeds: List[Embed] = [],
        allowed_mentions: AllowedMentions = None,
        tts: bool = False,
        flags: int = 64,
    ):
        state = self.bot._get_state()

        if embed and embeds:
            embeds.append(embed)
        elif embed:
            embeds = embed

        if embeds:
            embeds = list(map(lambda x: x.to_dict(), embeds))

        if allowed_mentions:
            if state.allowed_mentions:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()

        data = {
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "tts": tts,
            "flags": flags,
        }

        await self.bot.http.request(
            Route("POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"),
            json={"type": type, "data": data},
        )
