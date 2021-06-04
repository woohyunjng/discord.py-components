from discord.ext.commands import command, Cog
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


class ExampleCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def buttontest(self, ctx):
        await ctx.send(
            "Here is an example of a button",
            components=[
                [
                    Button(style=ButtonStyle.grey, label="EMOJI", emoji="😂"),
                    Button(style=ButtonStyle.green, label="GREEN"),
                    Button(style=ButtonStyle.red, label="RED"),
                    Button(style=ButtonStyle.grey, label="GREY", disabled=True),
                ],
                Button(style=ButtonStyle.blue, label="BLUE"),
                Button(
                    style=ButtonStyle.URL, label="URL", url="https://www.example.com"
                ),
            ],
        )

    @Cog.listener()
    async def on_button_click(self, res):
        """
        Possible interaction types:
        - Pong
        - ChannelMessageWithSource
        - DeferredChannelMessageWithSource
        - DeferredUpdateMessage
        - UpdateMessage
        """

        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f"{res.component.label} pressed",
        )


def setup(bot):
    DiscordComponents(
        bot
    )  # If you have this in an on_ready() event you can remove this line.
    bot.add_cog(ExampleCog(bot))
