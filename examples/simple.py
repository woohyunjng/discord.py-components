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
    stop = False
    while not stop:
        try:
            res = await bot.wait_for("button_click", check=check, timeout=60)
        except asyncio.TimeoutError:
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
                stop = True

bot.run("TOKEN")
