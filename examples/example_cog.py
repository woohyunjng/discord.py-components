import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

class examplecog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def buttontest(self, ctx):
        m = await ctx.send("Here is an example of a button",
                           components=[[

                               Button(style=ButtonStyle.grey, label="EMOJI", emoji="😂", disabled=True),
                               Button(style=ButtonStyle.green, label="GREEN"),
                               Button(style=ButtonStyle.red, label="RED"),
                               Button(style=ButtonStyle.grey, label="GREY"), ],

                               Button(style=ButtonStyle.blue, label="BLUE"),
                               Button(style=ButtonStyle.URL, label="URL", url="https://www.example.com"), ])
    @commands.Cog.listener()
    async def on_button_click(self, m):
        """Possible interaction types:
            Pong
            ChannelMessageWithSource
            DeferredChannelMessageWithSource
            DeferredUpdateMessage
            UpdateMessage

        """
        await m.respond(

            type=InteractionType.ChannelMessageWithSource,
            content=f'{m.component.label} pressed'
        )


def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(examplecog(bot))
