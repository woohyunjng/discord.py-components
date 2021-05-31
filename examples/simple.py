from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

bot = Bot("!")


@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")


@bot.command()
async def button(ctx):
    await ctx.send(
        "Here is an example of a button",
        components=[
            [
                Button(style=ButtonStyle.red, label="EMOJI", emoji="😂"),
                Button(style=ButtonStyle.green, label="GREEN"),
                Button(style=ButtonStyle.red, label="RED"),
                Button(style=ButtonStyle.grey, label="GREY", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="BLUE"),
            Button(style=ButtonStyle.URL, label="URL", url="https://www.example.com"),
        ],
    )


@bot.event
async def on_button_click(res):
    """
    Possible interaction types:
    - Pong
    - ChannelMessageWithSource
    - DeferredChannelMessageWithSource
    - DeferredUpdateMessage
    - UpdateMessage
    """

    await res.respond(
        type=InteractionType.ChannelMessageWithSource, content=f"{res.component.label} pressed"
    )


bot.run("TOKEN")
