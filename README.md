# discord.py-components
[![Build Status](https://travis-ci.com/kiki7000/discord.py-components.svg?branch=master)](https://travis-ci.com/kiki7000/discord.py-components)
[![PyPI version](https://badge.fury.io/py/discord-components.svg)](https://badge.fury.io/py/discord-components)
[![Documentation Status](https://readthedocs.org/projects/discord-components/badge/?version=latest)](https://discord-components.readthedocs.io/)

An unofficial library for Discord components. (on development)

- [GitHub](https://github.com/kiki7000/discord.py-components)
- [Discord Server](https://discord.gg/pKM6stqPxS)

## Installation
```sh
pip install --upgrade discord-components
```

## Example
```python
from discord import Client
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

bot = Client()

@bot.event
async def on_ready():
    DiscordComponents(bot)

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

    await msg.channel.send(
        "Content",
        components=[
            Button(style=ButtonStyle.blue, label="Blue"),
            Button(style=ButtonStyle.red, label="Red"),
            Button(style=ButtonStyle.URL, label="url", url="https://example.org"),
        ],
    )

    res = await bot.wait_for("button_click")
    if res.channel == msg.channel:
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f'{res.component.label} clicked'
        )
@bot.command()
async def buttons(ctx):
    """Buttons example with while and with check"""
    msg = await ctx.channel.send(embed=discord.Embed(color=discord.Color.random(), title="Navigation"),
                                 components=[
                                   [Button(style=ButtonStyle.blue, label="Backward", emoji="⏮️"),
                                    Button(style=ButtonStyle.red, label="Stop", emoji="❌"),
                                    Button(style=ButtonStyle.blue, label="Forward",  emoji="⏭️")]])

    def check(m):
        return m.user == ctx.author and m.message.channel == ctx.channel
    stop = False
    while not stop:
        res = await bot.wait_for("button_click", check=check)
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

bot.run("token")
```

## Docs
[The docs](https://discord-components.readthedocs.io/) can contain lot of spelling mistakes, grammar errors so if there is a problem please create an issue!

## Features
+ Send, edit Discord components.
+ Get components interact event!
+ Supports discord.py command extension.

## Helps
+ [Minibox](https://github.com/minibox24) - Button API explanation
+ [Lapis](https://github.com/Lapis0875) - Told me how to replace a property
