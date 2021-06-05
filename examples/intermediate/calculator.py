# By @Elektron-blip from https://gist.github.com/Elektron-blip/08fe25bd43e896d254d311721628d54f
import math
import datetime
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, DiscordComponents

client = commands.Bot(command_prefix="-")
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


@client.command()
async def calculator(ctx):
    expression = "None"
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    m = await ctx.send(
        components=buttons,
        embed=discord.Embed(
            title=f"{ctx.author.name}'s calculator",
            description=f"```xl\n{expression}```",
            timestamp=delta,
            color=discord.Colour.blurple(),
        ),
        reference=ctx.message,
    )
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
            await res.respond(
                embed=discord.Embed(
                    title=f"{ctx.author.name}'s calculator",
                    description=f"```xl\n{expression}```",
                    timestamp=delta,
                    color=discord.Colour.blurple(),
                ),
                components=buttons,
                type=7,
            )


client.run("YOUR_TOKEN")
