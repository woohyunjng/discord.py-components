# By @Elektron-blip in https://gist.github.com/Elektron-blip/08fe25bd43e896d254d311721628d54f
import math
import datetime
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_components import Button, ButtonStyle, DiscordComponents

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
dc = DiscordComponents(client)

buttons = [
    [
        Button(style=ButtonStyle.grey, label="1"),
        Button(style=ButtonStyle.grey, label="2"),
        Button(style=ButtonStyle.grey, label="3"),
        Button(style=ButtonStyle.blue, label="×"),
        Button(style=ButtonStyle.red, label="Exit"),
    ],
    [
        Button(style=ButtonStyle.grey, label="4"),
        Button(style=ButtonStyle.grey, label="5"),
        Button(style=ButtonStyle.grey, label="6"),
        Button(style=ButtonStyle.blue, label="÷"),
        Button(style=ButtonStyle.red, label="←"),
    ],
    [
        Button(style=ButtonStyle.grey, label="7"),
        Button(style=ButtonStyle.grey, label="8"),
        Button(style=ButtonStyle.grey, label="9"),
        Button(style=ButtonStyle.blue, label="+"),
        Button(style=ButtonStyle.red, label="Clear"),
    ],
    [
        Button(style=ButtonStyle.grey, label="00"),
        Button(style=ButtonStyle.grey, label="0"),
        Button(style=ButtonStyle.grey, label="."),
        Button(style=ButtonStyle.blue, label="-"),
        Button(style=ButtonStyle.green, label="="),
    ],
    [
        Button(style=ButtonStyle.grey, label="("),
        Button(style=ButtonStyle.grey, label=")"),
        Button(style=ButtonStyle.grey, label="π"),
        Button(style=ButtonStyle.grey, label="x²"),
        Button(style=ButtonStyle.grey, label="x³"),
    ],
]


def calculate(exp):
    o = exp.replace("×", "*")
    o = o.replace("÷", "/")
    o = o.replace("π", str(math.pi))
    o = o.replace("²", "**2")
    o = o.replace("³", "**3")
    result = ""
    try:
        result = str(eval(o))

    except:
        result = "An error occurred."

    return result


@slash.slash(
    name="calculator", description="A simple calculator. Can't do anything too complex."
)
async def calculator(ctx):
    m = await ctx.send(content="Loading Calculators...")
    expression = "None"
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    e = discord.Embed(
        title=f"{ctx.author.name}'s calculator",
        description=f"```xl\n{expression}```",
        timestamp=delta,
        color=discord.Colour.blurple(),
    )
    await m.edit(components=buttons, embed=e)
    while m.created_at < delta:
        res = await client.wait_for("button_click")
        if res.author.id == ctx.author.id and res.message.embeds[0].timestamp < delta:
            expression = res.message.embeds[0].description[6:-3]
            if expression == "None" or expression == "An error occurred.":
                expression = ""
            if res.component.label == "Exit":
                await res.respond(content="Calculator Closed", type=7)
                break
            elif res.component.label == "←":
                expression = expression[:-1]
            elif res.component.label == "Clear":
                expression = "None"
            elif res.component.label == "=":
                expression = calculate(expression)
            elif res.component.label == "x²":
                expression += "²"
            elif res.component.label == "x³":
                expression += "³"
            else:
                expression += res.component.label
            f = discord.Embed(
                title=f"{ctx.author.name}'s calculator",
                description=f"```xl\n{expression}```",
                timestamp=delta,
                color=discord.Colour.blurple(),
            )
            await res.respond(content="", embed=f, components=buttons, type=7)


client.run("Nzk4MTU4NjIyODA1OTgzMjUy.X_w9JA.4MZz4d3-0SGhEnu4D8_j3sCH-Rk")
