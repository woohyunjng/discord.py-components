from discord import Client, TextChannel
from discord.ext.commands import Bot

from typing import Union, List

from .buttonchannel import ButtonChannel


class DiscordButton:
    def __init__(self, bot: Union[Client, Bot]):
        self.bot = bot

        async def _send_button_textchannel(
            child_self, content: str = "", *, buttons: List["Button"] = None, **options
        ):
            await self.ButtonChannel(child_self).send(content, buttons=buttons, **options)

        TextChannel.send = _send_button_textchannel

    def ButtonChannel(self, channel: TextChannel):
        return ButtonChannel(self, channel)

    async def send_button(
        self, channel, content: str = "", *, buttons: List["Button"], options: dict = {}
    ):
        await self.ButtonChannel(channel).send(content, buttons=buttons, options=options)
