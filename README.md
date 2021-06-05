<div align="center">
    <a href="https://pypi.org/project/discord-components"><img src="https://raw.githubusercontent.com/kiki7000/discord.py-components/master/.github/logo.png" alt="discord-components logo" height="128" style="border-radius: 50%"></a>
    <div>
        <h1>discord-components</h1>
    </div>
    <div>
        <a href="https://travis-ci.com/kiki7000/discord.py-components"><img src="https://travis-ci.com/kiki7000/discord.py-components.svg?branch=master" alt="Build Status"></a>
        <a href="https://pypi.org/project/discord-components"><img src="https://badge.fury.io/py/discord-components.svg" alt="PyPI version"></a>
        <a href="https://pypi.org/project/discord-components"><img src="https://img.shields.io/pypi/dm/discord-components" alt="PyPI downloads"></a>
    </div>
    <div>
        <h3>An unofficial library for discord components (under-development)</h3>
    </div>
</div>

## Welcome!
Discord components are cool, but discord.py will support it on version 2.0. It is hard to wait, so we made a third-party library for using components such as buttons or selects!  We're currently developing this library, so it has a lot of bugs. But it has enough features to make the components easy to use :)

This project is open source ⭐.

Also, there is an [official discord server](https://discord.gg/pKM6stqPxS), so if you have a question, feel free to ask it on this server.

## Features
+ You can use discord components and handle interactions easily!
+ Methods based on discord.py.
+ Supports discord.ext.commands, and going to support [discord-py-slash-command](https://discord-py-slash-command.readthedocs.io/en/latest/).

## Docs
[The docs](https://devkiki7000.gitbook.io/discord-components/) could contain many grammatic errors, spelling mistakes, and typos because I am not a native English speaker. So if there is a problem on the docs, contact me or create an issue.

## Install
```
pip install --upgrade discord-components
```

## Example
```py
from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button

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
        ]
    )

    interaction = await bot.wait_for("button_click", check = lambda i: i.component.label.startswith("WOW"))
    await interaction.respond(content = "Button clicked!")


bot.run("your token")
```
You can see more examples [here](https://github.com/kiki7000/discord.py-components/tree/master/examples).

## License
This project is under the MIT License.

## Contribute
Anyone can contribute to this by forking the repository, making a change, and create a pull request!

But you have to follow these to PR.
+ Use the black formatter.
+ Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).
+ Test.

## Thanks to
+ [Minibox](https://github.com/minibox24) - Button API explanation when the button docs were only for beta users.
+ [Lapis](https://github.com/Lapis0875) - Suggested a method to change every class's property.
+ And to all contributors!
