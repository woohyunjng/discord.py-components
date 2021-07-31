<div align="center">
    <a href="https://pypi.org/project/discord-components"><img src="https://gitlab.com/uploads/-/system/project/avatar/27557052/logo.png?width=64" alt="discord-components logo" height="128" style="border-radius: 50%"></a>
    <div>
        <h1>discord-components</h1>
    </div>
    <div>
        <a href="https://travis-ci.com/kiki7000/discord.py-components"><img src="https://travis-ci.com/kiki7000/discord.py-components.svg?branch=master" alt="Build Status"></a>
        <a href="https://pypi.org/project/discord-components"><img src="https://badge.fury.io/py/discord-components.svg" alt="PyPI version"></a>
        <a href="https://pypi.org/project/discord-components"><img src="https://img.shields.io/pypi/dm/discord-components" alt="PyPI downloads"></a>
    </div>
    <div>
        <h3>An unofficial third party library or discord.py for discord components.</h3>
    </div>
</div>

## Welcome!
Discord components are cool, but discord.py will support it on version 2.0. It is hard to wait, so we made a third-party library for using components such as buttons or selects!

This project is open source ⭐.

Also, there is an [official discord server](https://discord.gg/pKM6stqPxS), so if you have any questions, feel free to ask it on this server.

## Features
+ You can use message components and handle component interactions easily!
+ Third-party of discord.py.

## Docs
+ [Gitbook version](https://devkiki7000.gitbook.io/discord-components) (Up to date)
+ [Sphinx Version](https://discord-components.readthedocs.io/en/0.5.2.4) (Currently outdated)

## Install
```
pip install --upgrade discord-components
```

## Example
```py
from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, Select, SelectOption

bot = Bot(command_prefix="your prefix")


@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")


@bot.command()
async def button(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Button(label="WOW button!", custom_id="button1")
        ]
    )

    interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id == "button1")
    await interaction.respond(content="Button clicked!")


@bot.command()
async def select(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Select(placeholder="select something!", options=[SelectOption(label="a", value="a"), SelectOption(label="b", value="b")], custom_id="select1")
        ]
    )

    interaction = await bot.wait_for("select_option", check = lambda i: i.component.custom_id == "select1")
    await interaction.respond(content = f"{interaction.component.values[0]} selected!")


bot.run("your token")
```
You can see more examples [here](https://gitlab.com/discord.py-components/discord.py-components/-/tree/master/examples).

## License
This project is under the MIT License.
