discord_buttons
==================================

unofficial library for discord buttons(on development)
`This <https://github.com/kiki7000/discord.py-buttons>`_ is the github repository


Install
--------

`pip install --upgrade discord_buttons`

Features
--------

- Send, Edit button messages
- Get button click event!
- Supports discord.ext.commands

Examples
--------

.. code:: python

    from discord import Client
    from discord_buttons import DiscordButton, Button, ButtonStyle, InteractionType

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
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f'{res.button.label} clicked'
        )


    bot.run("token")


Helps
--------
    
- `Minibox <https://github.com/minibox24>`_ - Button API explanation
- `Lapis <https://github.com/Lapis0875>`_ - Told me how to replace a property
