from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio

bot = Bot("!")


@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")


@bot.command()
async def waitforclick(ctx):
    m = await ctx.send(
        "Buttons waiting for a click",
        components=[
            Button(style=ButtonStyle.red, label="Click Me!"),
        ])

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        res = await bot.wait_for("button_click", check=check, timeout=15)
        await res.respond(
            type=InteractionType.ChannelMessageWithSource, content=f"{res.component.label} pressed"
        )

    except asyncio.TimeoutError:
        await m.edit(
            "Prompt timed out!",
            components=[
                Button(style=ButtonStyle.red, label="Timed out!", disabled=True),
            ]
        )


bot.run("TOKEN")
