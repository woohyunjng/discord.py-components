from discord.ext.commands import Bot
from discord_components import ComponentsBot, Button, ButtonStyle
from asyncio import TimeoutError

bot = ComponentsBot("!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


@bot.command()
async def wait_for_click(ctx):
    m = await ctx.send(
        "Buttons waiting for a click",
        components=[
            Button(style=ButtonStyle.red, label="Click Me!"),
        ],
    )

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        res = await bot.wait_for("button_click", check=check, timeout=15)
        await res.edit_origin(content=f"{res.component.label} pressed", components=[])

    except TimeoutError:
        await m.edit(
            "Prompt timed out!",
            components=[
                Button(style=ButtonStyle.red, label="Timed out!", disabled=True),
            ],
        )


bot.run("your token")
