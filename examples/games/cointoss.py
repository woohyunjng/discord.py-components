"""
@PythonSerious - 2021
"""

from discord import Embed
from discord.ext.commands import command, Cog
from discord_components import DiscordComponents, Button, ButtonStyle

from asyncio import TimeoutError, sleep
from random import choice


class Cointoss(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session_message = {}

    @command()
    async def cointoss(self, ctx):
        embed = Embed(
            color=0xF5F5F5,
            title=f"🪙 {ctx.author.name}'s coin toss 🪙",
            description="Pick heads or tails below!",
        )

        menu_components = [
            [
                Button(style=ButtonStyle.grey, label="Heads"),
                Button(style=ButtonStyle.grey, label="Tails"),
            ]
        ]
        heads_components = [
            [
                Button(style=ButtonStyle.green, label="Heads", disabled=True),
                Button(style=ButtonStyle.red, label="Tails", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="Play Again?", disabled=False),
        ]
        tails_components = [
            [
                Button(style=ButtonStyle.red, label="Heads", disabled=True),
                Button(style=ButtonStyle.green, label="Tails", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="Play Again?", disabled=False),
        ]

        if ctx.author.id in self.session_message:
            msg = self.session_message[ctx.author.id]
            await msg.edit(embed=embed, components=menu_components)
        else:
            msg = await ctx.send(embed=embed, components=menu_components)
            self.session_message[ctx.author.id] = msg

        def check(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=20)
        except TimeoutError:
            await msg.edit(
                embed=Embed(
                    color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"
                ),
                components=[
                    Button(
                        style=ButtonStyle.red,
                        label="Oh-no! Timeout reached!",
                        disabled=True,
                    )
                ],
            )
            return

        await res.respond(
            type=7,
            embed=Embed(
                color=0xF5F5F5,
                title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                description=f"You chose **{res.component.label.lower()}**!",
            ),
            components=menu_components,
        )

        game_choice = choice(["Heads", "Tails"])
        await sleep(2)

        if game_choice == res.component.label:
            embed = Embed(
                color=0x65DD65,
                title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                description=f"You chose **{res.component.label.lower()}**!\n\n> **YOU WIN!**",
            )
        else:
            embed = Embed(
                color=0xED564E,
                title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                description=f"You chose **{res.component.label.lower()}**!\n\n> You lost.",
            )

        await msg.edit(
            embed=embed,
            components=tails_components if game_choice == "Tails" else heads_components,
        )

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=20)
        except TimeoutError:
            await msg.delete()
            del self.session_message[ctx.author.id]
            return

        await res.respond(type=6)
        if res.component.label == "Play Again?":
            self.session_message[ctx.author.id] = msg
            await self.cointoss(ctx)


def setup(bot):
    DiscordComponents(bot)  # Remove this if you already have it in an on_ready event.
    bot.add_cog(Cointoss(bot))
