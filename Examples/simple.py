import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

bot = commands.Bot("!")

ddb = DiscordComponents(bot)

@bot.event
async def on_ready():   
  print(f'Logged in as {bot.user}!')


@bot.command()
async def button(ctx):
	m= await ctx.send("Here is an example of a button",
	components=[[
	Button(style=ButtonStyle.green, label="GREEN"),Button(style=ButtonStyle.red, label="RED"),
	Button(style=ButtonStyle.grey, label="GREY")],
	Button(style=ButtonStyle.blue, label="BLUE"),
	Button(style=ButtonStyle.URL, label="URL", url="https://www.example.com"),
	],
  )

@bot.event
async def on_button_click(m):
    await m.respond(
        type=InteractionType.ChannelMessageWithSource,
        content=f'{m.component.label} pressed'
    )

bot.run('TOKEN')
