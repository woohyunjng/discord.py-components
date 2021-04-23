from discord import TextChannel, Embed, File, AllowedMentions, InvalidArgument
from discord.http import Route

from aiohttp import ClientSession

from typing import List

from .button import Button


class ButtonChannel(TextChannel):
    def __init__(self, client: "DiscordButton", channel: TextChannel):
        self._client = client
        self._channel = channel
        super().__init__(
            state=channel._state,
            guild=channel.guild,
            data={
                "id": channel.id,
                "type": channel._type,
                "name": channel.name,
                "parent_id": channel.category_id,
                "topic": channel.topic,
                "position": channel.position,
                "nsfw": channel.nsfw,
                "rate_limit_per_user": channel.slowmode_delay,
                "last_message_id": channel.last_message_id,
            },
        )

    async def send(self, content: str = "", *, buttons: List[Button] = [], options: dict = {}):
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
            "options": options,
        }
        await self._client.bot.http.request(
            Route("POST", f"/channels/{self._channel.id}/messages"), json=data
        )
