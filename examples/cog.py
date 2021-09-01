from discord.ext.commands import command, Cog
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)


class ExampleCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def button(self, ctx):
        async def callback(interaction):
            await interaction.send(content="Yay")

        await ctx.send(
            "Button callbacks!",
            components=[
                self.bot.components_manager.add_callback(
                    Button(style=ButtonStyle.blue, label="Click this"), callback
                ),
            ],
        )

    @command()
    async def select(self, ctx):
        async def callback(interaction):
            await interaction.send(content="Yay")

        await ctx.send(
            "Select callbacks!",
            components=[
                self.bot.components_manager.add_callback(
                    Select(
                        options=[
                            SelectOption(label="a", value="a"),
                            SelectOption(label="b", value="b"),
                        ],
                    ),
                    callback,
                )
            ],
        )


def setup(bot):
    bot.add_cog(ExampleCog(bot))
