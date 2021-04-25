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
from .message import ButtonMessage


__all__ = ("DiscordButton",)


class DiscordButton:
    """discord_buttons client

    Parameters
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The bot
    change_discord_methods: :class:`bool`:
        Whether to change the methods of the discord module
        If this is enabled, you can just use `await <Messageable>.send`, `await <Context>.send` as `await <DiscordButton>.send_button_msg`

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

        async def send_button_msg_prop(ctxorchannel, *args, **kwargs) -> Message:
            if isinstance(ctxorchannel, DContext):
                return await self.send_button_msg(ctxorchannel.channel, *args, **kwargs)
            else:
                return await self.send_button_msg(ctxorchannel, *args, **kwargs)

        async def edit_button_msg_prop(*args, **kwargs):
            return await self.edit_button_msg(*args, **kwargs)

        async def wait_for_button_click_ctx(ctx, *args, **kwargs):
            return await self.wait_for_button_click(*args, **kwargs)

        Messageable.send = send_button_msg_prop
        Message.edit = edit_button_msg_prop
        DContext.wait_for_button_click = wait_for_button_click_ctx

    async def send_button_msg(
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
        """A function that sends a message with buttons

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
        buttons: List[Union[:class:`~discord_buttons.Button`, List[:class:`~discord_buttons.Button`]]]
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
        return ButtonMessage(buttons=buttons, state=state, channel=channel, data=data)

    async def edit_button_msg(
        self,
        message: ButtonMessage,
        content: str = "",
        *,
        tts: bool = False,
        embed: Embed = None,
        file: File = None,
        allowed_mentions: AllowedMentions = None,
        buttons: List[Button] = None,
        **options,
    ):

        """A function that edits a message with buttons

        :returns: :class:`discord_buttons.ButtonMessage`

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
        buttons: List[Union[:class:`~discord_buttons.Button`, List[:class:`~discord_buttons.Button`]]]
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

    async def wait_for_button_click(
        self,
        message: ButtonMessage,
        check: Callable[[Context], Awaitable[bool]] = None,
        timeout: float = None,
    ) -> Context:
        """A function that waits until a user clicks a button on the message

        :returns: :class:`~discord_buttons.Context`

        Parameters
        ----------
        message: :class:`~discord_buttons.ButtonMessage`
            The message
        check: Optional[Callable[[:class:`Context`], Coroutine[:class:`bool`]]]
            The wait_for check function
        timeout: Optional[:class:`float`]
            The wait_for timeout
        """
        while True:
            res = await self.bot.wait_for("socket_response", check=check, timeout=timeout)

            if res["t"] != "INTERACTION_CREATE":
                continue

            if message.id != int(res["d"]["message"]["id"]):
                continue
            break

        button_id = res["d"]["data"]["custom_id"]
        resbutton = None

        for buttons in res["d"]["message"]["components"]:
            for button in buttons["components"]:
                if button["style"] == 5:
                    continue

                if button["custom_id"] == button_id:
                    resbutton = button

        ctx = Context(
            bot=self.bot,
            client=self,
            user=User(state=self.bot._get_state(), data=res["d"]["member"]["user"]),
            button=Button(
                style=resbutton["style"],
                label=resbutton["label"],
                id=resbutton["custom_id"],
            ),
            raw_data=res,
            message=message,
        )
        return ctx

    async def fetch_button_message(self, message: Message) -> ButtonMessage:
        """Converts a message class to a ButtonMessage class

        :returns: :class:`~discord_butotns.ButtonMessage`

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

        return ButtonMessage(
            channel=message.channel, state=self.bot._get_state(), data=res, buttons=buttons
        )
