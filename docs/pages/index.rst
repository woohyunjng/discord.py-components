discord_components
==================================

unofficial library for discord components(on development)
`This <https://github.com/kiki7000/discord.py-components>`_ is the github repository


Install
--------

`pip install --upgrade discord-components`

Features
--------

- Send, Edit discord components
- Get components interact event!
- Supports discord.ext.commands

Examples
--------

.. code:: python

    from discord import Client
    from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

    bot = Client()
    ddb = DiscordComponents(bot)

    @bot.event
    async def on_message(msg):
        await msg.channel.send(
            "Content",
            components=[
                Button(style=ButtonStyle.blue, label="Blue"),
                Button(style=ButtonStyle.red, label="Red"),
                Button(style=ButtonStyle.URL, label="url", url="https://example.org"),
            ],
        )

        res = await ddb.wait_for_interact("button_click")
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
