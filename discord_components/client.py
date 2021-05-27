from discord import (
    Client,
    TextChannel,
    Message,
    Embed,
    AllowedMentions,
    InvalidArgument,
    User,
    File,
)
from discord.ext.commands import Bot, Context as DContext
from discord.http import Route
from discord.abc import Messageable

from functools import wraps
from asyncio import TimeoutError
from typing import Union, List, Callable, Awaitable
from json import dumps

from .button import Button
from .select import Select
from .component import Component
from .context import Context
from .message import ComponentMessage
from .interaction import InteractionEventType


__all__ = ("DiscordComponents",)


class DiscordComponents:
    """discord_components client

    Parameters
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The bot
    change_discord_methods: Optional[:class:`bool`]
        Default value set to True

        Whether to change the methods of the discord module
        If this is enabled, you can just use :class:`await <Messageable>.send`, :class:`await <Context>.send` as :class:`await <DiscordButton>.send_button_msg`, :class:`await <Message>.edit`, as :class:`await <DiscordComponents>.edit_component_msg`

    Attributes
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The bot
    """

    def __init__(self, bot, change_discord_methods=True):
        self.bot = bot
        if change_discord_methods:
            self.change_discord_methods()

    def change_discord_methods(self):
        """A function that change the methods of the discord module"""

        async def send_component_msg_prop(ctxorchannel, *args, **kwargs) -> Message:
            if isinstance(ctxorchannel, DContext):
                return await self.send_component_msg(ctxorchannel.channel, *args, **kwargs)
            else:
                return await self.send_component_msg(ctxorchannel, *args, **kwargs)

        async def edit_component_msg_prop(*args, **kwargs):
            return await self.edit_component_msg(*args, **kwargs)

        async def wait_for_interact_ctx(ctx, *args, **kwargs):
            return await self.wait_for_interact(*args, **kwargs)

        Messageable.send = send_component_msg_prop
        Message.edit = edit_component_msg_prop
        DContext.wait_for_interact = wait_for_interact_ctx

    async def send_component_msg(
        self,
        channel,
        content="",
        *,
        tts=False,
        embed=None,
        file=None,
        allowed_mentions=None,
        components=None,
        **options,
    ) -> Message:
        """A function that sends a message with components

        :returns: :class:`discord.Message`

        Parameters
        ----------
        channel: :class:`discord.Messageable`
            The channel to send the message
        content: str
            The message's content
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        embed: :class:`discord.Embed`
            The rich embed for the content.
        file: :class:`discord.File`
            The file to upload.
        allowed_mentions: :class:`discord.AllowedMentions`
            Controls the mentions being processed in this message. If this is
            passed, then the object is merged with :attr:`discord.Client.allowed_mentions`.
            The merging behaviour only overrides attributes that have been explicitly passed
            to the object, otherwise it uses the attributes set in :attr:`discord.Client.allowed_mentions`.
            If no object is passed at all then the defaults given by :attr:`discord.Client.allowed_mentions`
            are used instead.
        components: List[Union[:class:`~discord_components.Component`, List[:class:`~discord_components.Component`]]]
            The components to send.
            If this is 2-dimensional array, an array is a line
        """
        state = self.bot._get_state()

        if embed:
            embed = embed.to_dict()

        if allowed_mentions:
            if state.allowed_mentions:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()

        data = {
            "content": content,
            **self._get_components_json(components),
            **options,
            "embed": embed,
            "allowed_mentions": allowed_mentions,
            "tts": tts,
        }

        if file:
            try:
                await self.bot.http.request(
                    Route("POST", f"/channels/{channel.id}/messages"),
                    form=[
                        {
                            "name": "payload_json",
                            "value": dumps(data, separators=(",", ":"), ensure_ascii=True),
                        },
                        {
                            "name": "file",
                            "value": file.fp,
                            "filename": file.filename,
                            "content_type": "application/octet-stream",
                        },
                    ],
                    files=[file],
                )
            finally:
                file.close()
        else:
            data = await self.bot.http.request(
                Route("POST", f"/channels/{channel.id}/messages"), json=data
            )
        return ComponentMessage(components=components, state=state, channel=channel, data=data)

    async def edit_component_msg(
        self,
        message,
        content="",
        *,
        tts=False,
        embed=None,
        file=None,
        allowed_mentions=None,
        components=None,
        **options,
    ):

        """A function that edits a message with components

        :returns: :class:`discord_components.ComponentMessage`

        Parameters
        ----------
        channel: :class:`discord.Messageable`
            The channel to send the message
        content: str
            The message's content
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        embed: :class:`discord.Embed`
            The rich embed for the content.
        file: :class:`discord.File`
            The file to upload.
        allowed_mentions: :class:`discord.AllowedMentions`
            Controls the mentions being processed in this message. If this is
            passed, then the object is merged with :attr:`discord.Client.allowed_mentions`.
            The merging behaviour only overrides attributes that have been explicitly passed
            to the object, otherwise it uses the attributes set in :attr:`discord.Client.allowed_mentions`.
            If no object is passed at all then the defaults given by :attr:`discord.Client.allowed_mentions`
            are used instead.
        components: List[Union[:class:`~discord_components.Component`, List[:class:`~discord_components.Component`]]]
            The components to send.
            If this is 2-dimensional array, an array is a line
        """
        state = self.bot._get_state()

        if embed:
            embed = embed.to_dict()

        if allowed_mentions:
            if state.allowed_mentions:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()

        data = {
            "content": content,
            **self._get_components_json(components),
            **options,
            "embed": embed,
            "allowed_mentions": allowed_mentions,
            "tts": tts,
        }
        if file:
            try:
                await self.bot.http.request(
                    Route("PATCH", f"/channels/{message.channel.id}/messages/{message.id}"),
                    form=[
                        {
                            "name": "payload_json",
                            "value": dumps(data, separators=(",", ":"), ensure_ascii=True),
                        },
                        {
                            "name": "file",
                            "value": file.fp,
                            "filename": file.filename,
                            "content_type": "application/octet-stream",
                        },
                    ],
                    files=[file],
                )
            finally:
                file.close()
        else:
            await self.bot.http.request(
                Route("PATCH", f"/channels/{message.channel.id}/messages/{message.id}"), json=data
            )

    def _get_components_json(
        self, components: List[Union[Component, List[Component]]] = None
    ) -> dict:
        if not components:
            return {}

        for i in range(len(components)):
            if not isinstance(components[i], list):
                components[i] = [components[i]]

        lines = components
        return {
            "components": (
                [
                    {
                        "type": 1,
                        "components": [component.to_dict() for component in components],
                    }
                    for components in lines
                ]
                if lines
                else []
            ),
        }

    def _get_component_type(self, type: int):
        if type == 2:
            return Button
        elif type == 3:
            return Select

    def _structured_raw_data(self, raw_data: dict) -> dict:
        data = {
            "interaction": raw_data["d"]["id"],
            "interaction_token": raw_data["d"]["token"],
            "raw": raw_data,
        }
        raw_data = raw_data["d"]
        state = self.bot._get_state()

        components = []
        for line in raw_data["message"]["components"]:
            if line["type"] >= 2:
                components.append(self._get_component_type(line["type"]).from_json(line))
            for btn in line["components"]:
                if btn["type"] >= 2:
                    components.append(self._get_component_type(btn["type"]).from_json(btn))

        data["message"] = ComponentMessage(
            state=state,
            channel=self.bot.get_channel(int(raw_data["channel_id"])),
            data=raw_data["message"],
            components=components,
        )

        if "member" in raw_data:
            userData = raw_data["member"]["user"]
        else:
            userData = raw_data["user"]
        data["user"] = User(state=state, data=userData)
        data["custom_id"] = raw_data["data"]["custom_id"]

        return data

    async def wait_for_interact(
        self,
        type,
        check=None,
        timeout=None,
    ) -> Context:
        """A function that waits until a user clicks a button on the message

        :returns: :class:`~discord_components.Context`

        Parameters
        ----------
        type: :class:`str`
            The interaction event type
        check: Optional[Callable[[:class:`Context`], Coroutine[:class:`bool`]]]
            The wait_for check function
        timeout: Optional[:class:`float`]
            The wait_for timeout
        """

        while True:
            res = await self.bot.wait_for("socket_response", check=check, timeout=timeout)

            if res["t"] != "INTERACTION_CREATE":
                continue

            if InteractionEventType[type] != res["d"]["data"]["component_type"]:
                continue

            break

        data = self._structured_raw_data(res)
        rescomponent = None

        for component in data["message"].components:
            if component.id == data["custom_id"]:
                rescomponent = component

        ctx = Context(
            bot=self.bot,
            client=self,
            user=data["user"],
            component=rescomponent,
            raw_data=data["raw"],
            message=data["message"],
        )
        return ctx

    async def fetch_component_message(self, message) -> ComponentMessage:
        """Converts a message class to a ComponentMessage class

        :returns: :class:`~discord_components.ComponentMessage`

        Parameters
        ----------
        message: :class:`discord.Message`
            The message to convert
        """

        res = await self.bot.http.request(
            Route("GET", f"/channels/{message.channel.id}/messages/{message.id}")
        )
        components = []

        for i in res["components"]:
            if i["type"] >= 2:
                components.append(self._get_component_type(i["type"]).from_json(i))
                continue

            for j in i["components"]:
                if j["type"] < 2:
                    continue
                components.append(self._get_component_type(i["type"]).from_json(i))

        return ComponentMessage(
            channel=message.channel, state=self.bot._get_state(), data=res, components=components
        )
