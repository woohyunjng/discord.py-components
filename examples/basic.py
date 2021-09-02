from discord_components import Button, Select, SelectOption, ComponentsBot


bot = ComponentsBot("!")
"""
or you can just override the methods yourself

bot = discord.ext.commands.Bot("!")
DiscordComponents(bot)
"""


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


@bot.command()
async def button(ctx):
    await ctx.send("Buttons!", components=[Button(label="Button", custom_id="button1")])
    interaction = await bot.wait_for(
        "button_click", check=lambda inter: inter.custom_id == "button1"
    )
    await interaction.send(content="Button Clicked")


@bot.command()
async def select(ctx):
    await ctx.send(
        "Selects!",
        components=[
            Select(
                placeholder="Select something!",
                options=[
                    SelectOption(label="a", value="a"),
                    SelectOption(label="b", value="b"),
                ],
                custom_id="select1",
            )
        ],
    )

    interaction = await bot.wait_for(
        "select_option", check=lambda inter: inter.custom_id == "select1"
    )
    await interaction.send(content=f"{interaction.values[0]} selected!")


bot.run("your token")
