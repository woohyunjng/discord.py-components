from typing import List

from discord.abc import Messageable
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption,
    Interaction,
)


class Paginator:
    def __init__(
        self,
        client: DiscordComponents,
        channel: Messageable,
        contents: List[str],
        use_select: bool = False,
    ):
        self.client = client
        self.channel = channel
        self.contents = contents
        self.use_select = use_select
        self.index = 0

    def get_components(self):
        if self.use_select:
            return [
                self.client.add_callback(
                    Select(
                        custom_id="paginator_select",
                        options=[
                            SelectOption(label=f"Page {i}", value=str(i), default=i == self.index)
                            for i in range(len(self.contents))
                        ],
                    ),
                    self.select_callback,
                )
            ]
        else:
            return [
                [
                    self.client.add_callback(
                        Button(style=ButtonStyle.blue, emoji="◀️"), self.button_left_callback
                    ),
                    Button(label=f"Page {self.index + 1}/{len(self.contents)}", disabled=True),
                    self.client.add_callback(
                        Button(style=ButtonStyle.blue, emoji="▶️"), self.button_right_callback
                    ),
                ]
            ]

    async def start(self):
        self.msg = await self.channel.send(
            self.contents[self.index], components=self.get_components()
        )

    async def select_callback(self, inter: Interaction):
        self.index = int(inter.values[0])
        await inter.edit_origin(content=self.contents[self.index], components=self.get_components())

    async def button_left_callback(self, inter: Interaction):
        if self.index == 0:
            self.index = len(self.contents) - 1
        else:
            self.index -= 1

        await self.button_callback(inter)

    async def button_right_callback(self, inter: Interaction):
        if self.index == len(self.contents) - 1:
            self.index = 0
        else:
            self.index += 1

        await self.button_callback(inter)

    async def button_callback(self, inter: Interaction):
        await inter.edit_origin(content=self.contents[self.index], components=self.get_components())
