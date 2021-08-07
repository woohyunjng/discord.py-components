from typing import Union

from discord import (
    Client,
    Message,
    User,
    Guild,
)
from discord.ext.commands import Bot
from discord.abc import Messageable

from .component import Component
from .http import HTTPClient
from .interaction import Interaction, InteractionEventType

from .ext.filters import *

__all__ = ("DiscordComponents",)


class DiscordComponents:
    def __init__(
        self,
        bot: Union[Bot, Client],
    ):
        self.bot = bot
        self.http = HTTPClient(bot=bot)

        if isinstance(self.bot, Bot):
            self.bot.add_listener(self.on_socket_response, name="on_socket_response")
        else:
            self.bot.on_socket_response = self.on_socket_response

    async def on_socket_response(self, res):
        if (res["t"] != "INTERACTION_CREATE") or (res["d"]["type"] != 3):
            return

        for _type in InteractionEventType:
            if _type.value == res["d"]["data"]["component_type"]:
                self.bot.dispatch(f"raw_{_type.name}", res["d"])
                self.bot.dispatch(_type.name, self._get_interaction(res))
                break

    def _get_interaction(self, json: dict):
        ctx = Interaction(
            state=self.bot._connection,
            client=self,
            raw_data=json["d"],
        )
        return ctx

    async def wait_for(
        self,
        event: str,
        *,
        message: Message = None,
        component: Component = None,
        ephemeral: bool = False,
        guild: Guild = None,
        channel: Messageable = None,
        user: User = None,
        timeout: float = None,
    ):
        check_list = []
        if message is not None:
            check_list.append(message_filter(message, ephemeral))
        if component is not None:
            check_list.append(component_filter(component))
        if guild is not None:
            check_list.append(guild_filter(guild))
        if channel is not None:
            check_list.append(channel_filter(channel))
        if user is not None:
            check_list.append(user_filter(user))

        def check(interaction: Interaction):
            for i in check_list:
                if not i(interaction):
                    return False
            return True

        return await self.bot.wait_for(event, check=check, timeout=timeout)
