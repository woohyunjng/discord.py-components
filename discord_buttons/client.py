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
from typing import Union, List
from json import dumps

from .button import Button
from .context import Context


__all__ = ("DiscordButton",)


class DiscordButton:
    def __init__(self, bot: Union[Client, Bot]):
        self.bot = bot

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
        return Message(state=state, channel=channel, data=data)

    async def edit_button_msg(
        self,
        message: Message,
        content: str = "",
        *,
        tts: bool = False,
        embed: Embed = None,
        file: File = None,
        allowed_mentions: AllowedMentions = None,
        buttons: List[Button] = None,
        **options,
    ):
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

    async def wait_for_button_click(self, message: Message, check=None, timeout: float = None):
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
