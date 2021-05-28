discord_components
==================================

Unofficial library for Discord components. (on development)

- `GitHub <https://github.com/kiki7000/discord.py-components>`_
- `Discord Server <https://discord.gg/pKM6stqPxS>`_


Install
--------

`pip install --upgrade discord-components`

Features
--------

- Send, edit Discord components.
- Get components interact event!
- Supports discord.py command extension.

Examples
--------

.. code:: python

    from discord import Client
    from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

    bot = Client()
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


    bot.run("token")


Helps
--------
    
- `Minibox <https://github.com/minibox24>`_ - Button API explanation
- `Lapis <https://github.com/Lapis0875>`_ - Told me how to replace a property
