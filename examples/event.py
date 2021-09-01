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


@bot.event
async def on_button_click(interaction):
    await interaction.respond(content="Button Clicked")


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


@bot.event
async def on_select_option(interaction):
    await interaction.respond(content=f"{interaction.values[0]} selected!")


@bot.command()
async def interaction(ctx):
    await ctx.send(
        "Buttons and Selects!",
        components=[
            Select(
                placeholder="Select something!",
                options=[
                    SelectOption(label="a", value="a"),
                    SelectOption(label="b", value="b"),
                ],
                custom_id="select1",
            ),
            Button(label="Button", custom_id="button1"),
        ],
    )


@bot.event
async def on_interaction(interaction):
    if interaction.custom_id not in ["select1", "button1"]:
        return

    if isinstance(interaction.component, Button):
        await interaction.respond(content="Button clicked!")
    else:
        await interaction.respond(content=f"{interaction.values[0]} selected!")


bot.run("your token")
