from discord import Client, TextChannel, Message, Embed, AllowedMentions, InvalidArgument, User
from discord.ext.commands import Bot, Context as DContext
from discord.http import Route
from discord.abc import Messageable

from functools import wraps
from asyncio import TimeoutError
from typing import Union, List

from .button import Button
from .context import Context


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

        async def wait_for_button_click_ctx(_s, *args, **kwargs):
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
        await self.bot.http.request(
            Route("PATCH", f"/channels/{message.channel.id}/messages/{message.id}"), json=data
        )

    def _get_buttons_json(self, buttons: List[Union[Button, List[Button]]] = None) -> dict:
        if not buttons:
            return {"components": []}

        if isinstance(buttons[0], Button):
            buttons = [buttons]

        lines = buttons
        return {
            "components": (
                [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "style": button.style,
                                "label": button.label,
                                "custom_id": button.id,
                                "url": button.url,
                            }
                            for button in buttons
                        ],
                    }
                    for buttons in lines
                ]
                if buttons
                else []
            ),
        }

    async def wait_for_button_click(self, message: Message, check=None, timeout: float = None):
        res = await self.bot.wait_for("socket_response", check=check, timeout=timeout)

        if res["t"] != "INTERACTION_CREATE":
            return None

        button_id = res["d"]["data"]["custom_id"]
        resbutton = None

        for buttons in res["d"]["message"]["components"]:
            for button in buttons["components"]:
                if button["style"] == 5:
                    continue

                if button["custom_id"] == button_id:
                    resbutton = button

        ctx = Context(
            message=message,
            user=User(state=self.bot._get_state(), data=res["d"]["member"]["user"]),
            button=Button(
                style=resbutton["style"],
                label=resbutton["label"],
                id=resbutton["custom_id"],
            ),
            interaction_id=res["d"]["id"],
            raw_data=res,
        )
        return ctx
