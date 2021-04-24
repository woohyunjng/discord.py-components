# discord.py-buttons
[![Build Status](https://travis-ci.com/kiki7000/discord.py-buttons.svg?branch=main)](https://travis-ci.com/kiki7000/discord.py-buttons)
[![PyPI version](https://badge.fury.io/py/discord-buttons.svg)](https://badge.fury.io/py/discord-buttons)

unofficial library for discord buttons(on development)

## Install
```sh
pip install --upgrade discord_buttons
```

## Example
```python
from discord import Client
from discord_buttons import DiscordButton, Button, ButtonStyle

bot = Client()
ddb = DiscordButton(bot)

@bot.event
async def on_message(msg):
    m = await msg.channel.send(
        "Content",
        buttons=[
            Button(style=ButtonStyle.blue, label="Blue"),
            Button(style=ButtonStyle.red, label="Red"),
            Button(style=ButtonStyle.URL, label="url", url="https://example.org"),
        ],
    )
    res = await ddb.wait_for_button_click(m)
    await msg.channel.send(f'{res.button.label} clicked')


bot.run("token")
```

## Features
+ Send, Edit button messages
+ Get button click event!
+ Supports discord.ext.commands

## Helps
+ [Minibox](https://github.com/minibox24) - Button API explanation
+ [Lapis](https://github.com/Lapis0875) - Told me how to replace a property