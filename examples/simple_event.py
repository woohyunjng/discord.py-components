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
    components = [Button(label="Button", custom_id="button1")]

    await ctx.send("Buttons!", components=components)


@bot.event
async def on_button_click(interaction):
    await interaction.respond(content="Button Clicked")


@bot.command()
async def select(ctx):
    components = [
        Select(
            placeholder="Select something!",
            options=[
                SelectOption(label="a", value="a"),
                SelectOption(label="b", value="b"),
            ],
            custom_id="select1",
        )
    ]

    await ctx.send("Selects!",components=components)


@bot.event
async def on_select_option(interaction):
    await interaction.respond(content=f"{interaction.values[0]} selected!")

