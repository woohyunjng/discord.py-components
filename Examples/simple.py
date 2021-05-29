import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

bot = commands.Bot("!")




@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f'Logged in as {bot.user}!')


@bot.command()
async def button(ctx):
    m = await ctx.send("Here is an example of a button",
            components=[[
                Button(style=ButtonStyle.red, label="EMOJI", emoji="😂", disabled=True),
                Button(style=ButtonStyle.green, label="GREEN"), Button(style=ButtonStyle.red, label="RED"),
                Button(style=ButtonStyle.grey, label="GREY"), ],

                Button(style=ButtonStyle.blue, label="BLUE"),
                Button(style=ButtonStyle.URL, label="URL", url="https://www.example.com"),
             ])


@bot.event
async def on_button_click(m):
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


bot.run('TOKEN')
