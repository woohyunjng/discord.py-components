from discord import Client, TextChannel, Message
from discord.ext.commands import Bot
from discord.http import Route

from typing import Union, List

from .button import Button


class DiscordButton:
    def __init__(self, bot: Union[Client, Bot]):
        self.bot = bot

        async def send_button_msg_prop(
            chan: TextChannel, content: str = "", *, buttons: List[Button] = None, **options
        ) -> Message:
            return await self.send_button_msg(chan, content, buttons=buttons, **options)

        async def edit_button_msg_prop(
            message: Message, content: str = "", *, buttons: List[Button] = None, **options
        ):
            return await self.edit_button_msg(message, content, buttons=buttons, **options)

        TextChannel.send = send_button_msg_prop
        Message.edit = edit_button_msg_prop

    async def send_button_msg(
        self, channel: TextChannel, content: str = "", *, buttons: List[Button] = None, **options
    ) -> Message:
        data = {
            "content": content,
            **self._get_buttons_json(buttons),
            **options,
        }
        data = await self.bot.http.request(
            Route("POST", f"/channels/{channel.id}/messages"), json=data
        )
        return Message(state=self.bot._get_state(), channel=channel, data=data)

    async def edit_button_msg(
        self, message: Message, content: str = "", *, buttons: List[Button] = None, **options
    ):
        data = {
            "content": content,
            **self._get_buttons_json(buttons),
            **options,
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
        print(lines)
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
