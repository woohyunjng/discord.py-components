---
description: Unofficial library for Discord components. (on development)
---

# Getting started

## Welcome~!

Discord components are cool, but discord.py will support it on version 2.0. It is hard to wait, so we made a third-party library for using components such as buttons or selects!  We're currently developing this library, so it has a lot of bugs. But it has enough features to make the components easy to use :\)

So let's use this library. First, we need to install the library

```bash
pip install --upgrade discord-components
```

Assuming you have invited your bot to some server, let's code.  Create any python file and copy & paste that. \(with replacing `your token` with your bot's token and `your prefix` with your bot's prefix\) 

{% code title="bot.py" %}
```python
from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

bot = Bot(command_prefix = "your prefix")


@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")


@bot.command()
async def button(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Button(label = "WOW button!")
        ],
    )


bot.run("your token")
```
{% endcode %}

