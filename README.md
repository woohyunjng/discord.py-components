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
from discord_buttons import DiscordButton, Button

bot = Client()
DiscordButton(bot)

@bot.event
async def on_message(msg):
    await msg.channel.send(
        "Content",
        buttons=[
            Button(style="blue", label="Blue"),
            Button(style="red", label="Red"),
            Button(style="url", label="url", url="https://example.org"),
        ],
    )


bot.run("token")
```

## Features
+ Send, Edit button messages
+ Get button click event!

## Helps
+ [Minibox](https://github.com/minibox24) - Button API explanation