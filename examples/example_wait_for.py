from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from asyncio import TimeoutError

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
        ],
    )

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        res = await bot.wait_for("button_click", check=check, timeout=15)
        await res.respond(
            type=InteractionType.ChannelMessageWithSource, content=f"{res.component.label} pressed"
        )

    except TimeoutError:
        await m.edit(
            "Prompt timed out!",
            components=[
                Button(style=ButtonStyle.red, label="Timed out!", disabled=True),
            ],
        )
  
@bot.command()
async def buttons(ctx):
    """Buttons example of navigation with while and with check"""
    msg = await ctx.channel.send(embed=discord.Embed(color=discord.Color.random(), title="Navigation"),
                                 components=[
                                   [Button(style=ButtonStyle.blue, label="Backward", emoji="⏮️"),
                                    Button(style=ButtonStyle.red, label="Stop", emoji="❌"),
                                    Button(style=ButtonStyle.blue, label="Forward",  emoji="⏭️")]])
    def check(m):
        return m.user == ctx.author and m.message.channel == ctx.channel
    while True:
        try:
            res = await bot.wait_for("button_click", check=check, timeout=60)
        except asyncio.TimeoutError:
            break
            await msg.delete()
            return await ctx.send(embed=discord.Embed(color=discord.Color.red(),
                                                      title="TImeout"))
        if res.channel == ctx.channel:
            if res.component.label == "Forward":
                await msg.edit(embed=discord.Embed(color=discord.Color.random(),
                                                   title="Forward"))
                await res.respond(
                    type=InteractionType.DeferredUpdateMessage
                )
            elif res.component.label == "Backward":
                await msg.edit(embed=discord.Embed(color=discord.Color.random(),
                                                   title="Backward"))
                await res.respond(
                    type=InteractionType.DeferredUpdateMessage
                )
            elif res.component.label == "Stop":
                await msg.edit(embed=discord.Embed(color=discord.Color.random(),
                                                   title="Stop"))
                await res.respond(
                    type=InteractionType.UpdateMessage
                )
                await msg.delete()


bot.run("TOKEN")
