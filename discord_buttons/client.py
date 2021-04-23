from discord import Client, TextChannel, Message
from discord.ext.commands import Bot
from discord.http import Route

from typing import Union, List


class DiscordButton:
    def __init__(self, bot: Union[Client, Bot]):
        self.bot = bot

        async def send_button_prop(
            chan, content: str = "", *, buttons: List["Button"] = None, **options
        ):
            return await self.send_button(chan, content, buttons=buttons, **options)

        TextChannel.send = send_button_prop

    async def send_button(
        self, channel, content: str = "", *, buttons: List["Button"] = None, **options
    ):
        data = {
            "content": content,
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
                ]
                if buttons
                else []
            ),
            **options,
        }
        data = await self.bot.http.request(
            Route("POST", f"/channels/{channel.id}/messages"), json=data
        )
        return Message(state=self.bot._get_state(), channel=channel, data=data)
