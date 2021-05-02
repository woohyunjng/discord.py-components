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
    change_discord_methods: :class:`bool`
        Whether to change the methods of the discord module
        If this is enabled, you can just use :class:`await <Messageable>.send`, :class:`await <Context>.send` as :class:`await <DiscordButton>.send_button_msg`, :class:`await <Message>.edit`, as :class:`await <DiscordComponents>.edit_component_msg`

    Attributes
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The bot
    """

    def __init__(self, bot: Union[Client, Bot], change_discord_methods: bool = True):
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
        channel: TextChannel,
        content: str = "",
        *,
        tts: bool = False,
        embed: Embed = None,
        file: File = None,
        allowed_mentions: AllowedMentions = None,
        buttons: List[Button] = None,
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
        buttons: List[Union[:class:`~discord_components.Button`, List[:class:`~discord_components.Button`]]]
            The buttons to send.
            If this is 2-dimensional array, a array is a line
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
            **self._get_buttons_json(buttons),
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
        return ComponentMessage(buttons=buttons, state=state, channel=channel, data=data)

    async def edit_component_msg(
        self,
        message: ComponentMessage,
        content: str = "",
        *,
        tts: bool = False,
        embed: Embed = None,
        file: File = None,
        allowed_mentions: AllowedMentions = None,
        buttons: List[Button] = None,
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
        buttons: List[Union[:class:`~discord_components.Button`, List[:class:`~discord_components.Button`]]]
            The buttons to send.
            If this is 2-dimensional array, a array is a component group
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
            **self._get_buttons_json(buttons),
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

    def _get_buttons_json(self, buttons: List[Union[Button, List[Button]]] = None) -> dict:
        if not buttons:
            return {}

        if isinstance(buttons[0], Button):
            buttons = [buttons]

        lines = buttons
        return {
            "components": (
                [
                    {
                        "type": 1,
                        "components": [button.to_dict() for button in buttons],
                    }
                    for buttons in lines
                ]
                if buttons
                else []
            ),
        }

    def _structured_raw_data(self, raw_data: dict) -> dict:
        data = {
            "interaction": raw_data["d"]["id"],
            "interaction_token": raw_data["d"]["token"],
            "raw": raw_data,
        }
        raw_data = raw_data["d"]
        state = self.bot._get_state()

        buttons = []
        for line in raw_data["message"]["components"]:
            if line["type"] == 2:
                buttons.append(Button.from_json(line))
            for btn in line["components"]:
                if btn["type"] == 2:
                    buttons.append(Button.from_json(btn))

        data["message"] = ComponentMessage(
            state=state,
            channel=self.bot.get_channel(int(raw_data["channel_id"])),
            data=raw_data["message"],
            buttons=buttons,
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
        type: Union["button_click"],
        check: Callable[[Context], Awaitable[bool]] = None,
        timeout: float = None,
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
        resbutton = None

        for btn in data["message"].buttons:
            if btn.id == data["custom_id"]:
                resbutton = btn

        ctx = Context(
            bot=self.bot,
            client=self,
            user=data["user"],
            component=resbutton,
            raw_data=data["raw_data"],
            message=data["message"],
        )
        return ctx

    async def fetch_button_message(self, message: Message) -> ComponentMessage:
        """Converts a message class to a ComponentMessage class

        :returns: :class:`~discord_butotns.ComponentMessage`

        Parameters
        ----------
        message: :class:`discord.Message`
            The message to convert
        """

        res = await self.bot.http.request(
            Route("GET", f"/channels/{message.channel.id}/messages/{message.id}")
        )
        buttons = []

        for i in res["components"]:
            if i["type"] == 2:
                r = {}
                if "custom_id" in i.keys():
                    r["id"] = i["custom_id"]
                if "url" in i.keys():
                    r["url"] = i["url"]
                buttons.append(Button(style=i["style"], label=i["label"], **r))
                continue

            for j in i["components"]:
                if j["type"] != 2:
                    continue

                r = {}
                if "custom_id" in j.keys():
                    r["id"] = j["custom_id"]
                if "url" in j.keys():
                    r["url"] = j["url"]
                buttons.append(Button(style=j["style"], label=j["label"], **r))

        return ComponentMessage(
            channel=message.channel, state=self.bot._get_state(), data=res, buttons=buttons
        )
