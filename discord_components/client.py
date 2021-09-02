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

__all__ = ("DiscordComponents", "ComponentsClient", "ComponentsBot")


class DiscordComponents:
    def __init__(
        self,
        bot: Union[Bot, Client],
    ):
        self.bot = bot
        bot.components_manager = self

        self.http = HTTPClient(bot=bot)
        self._components_callback = {}

        if isinstance(self.bot, Bot):
            self.bot.add_listener(self.on_socket_response, name="on_socket_response")
        else:
            self.bot.on_socket_response = self.on_socket_response

    async def on_socket_response(self, res):
        if (res["t"] != "INTERACTION_CREATE") or (res["d"]["type"] != 3):
            return

        if res["d"]["message"].get("message_reference") and not res["d"]["message"][
            "message_reference"
        ].get("channel_id"):
            res["d"]["message"]["message_reference"] = res["d"]["channel_id"]

        interaction = self._get_interaction(res)
        self.bot.dispatch(f"raw_interaction", res["d"])
        self.bot.dispatch("interaction", interaction)

        if self._components_callback.get(interaction.custom_id):
            callback_info = self._components_callback[interaction.custom_id]
            if callback_info["uses"] == 0:
                del self._components_callback[interaction.custom_id]
                return

            if callback_info["uses"] is not None:
                self._components_callback[interaction.custom_id]["uses"] -= 1
            if not callback_info["filter"](interaction):
                return

            await self._components_callback[interaction.custom_id]["callback"](interaction)

        for _type in InteractionEventType:
            if _type.value == res["d"]["data"]["component_type"]:
                self.bot.dispatch(f"raw_{_type.name}", res["d"])
                self.bot.dispatch(_type.name, interaction)
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

    def add_callback(self, component: Component, callback, *, uses: int = None, filter=None):
        self._components_callback[component.custom_id] = {
            "callback": callback,
            "uses": uses,
            "filter": filter or (lambda x: True),
        }
        return component


class ComponentsClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components_manager = DiscordComponents(self)


class ComponentsBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components_manager = DiscordComponents(self)
