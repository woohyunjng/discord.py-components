import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio
import random


class calc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.authorized = [533069055784124437, 329035513665290240, 460617153759150101, 169899942658179072,
                           464586638576582678,
                           432690287484207105, 660237012283949086, 505478212990795787, 510758899985547266,
                           475371795185139712,
                           383907659947966466, 692787014193381419]

    @commands.command()
    async def cointoss(self, ctx):
        async def cointoss1(m=False):
            if ctx.author.id in self.authorized or "Tester" in str(
                    ctx.author.roles) or ctx.channel.id == 848824138319659009:
                embed = discord.Embed(color=0xf5f5f5, title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                                      description="Pick heads or tails below!")

                components = [

                    [
                        Button(style=ButtonStyle.grey, label='Heads'),
                        Button(style=ButtonStyle.grey, label='Tails'),
                    ]

                ]
                heads = [

                    [
                        Button(style=ButtonStyle.green, label='Heads', disabled=True),
                        Button(style=ButtonStyle.red, label='Tails', disabled=True),
                    ],
                    Button(style=ButtonStyle.blue, label='Play Again?', disabled=False),

                ]
                tails = [

                    [
                        Button(style=ButtonStyle.red, label='Heads', disabled=True),
                        Button(style=ButtonStyle.green, label='Tails', disabled=True),
                    ],
                    Button(style=ButtonStyle.blue, label='Play Again?', disabled=False),

                ]
                if m:
                    print("m given")
                    await m.edit(embed=embed, components=components)
                if not m:
                    print("no M")
                    m = await ctx.send(embed=embed, components=components)

                def check(res):
                    return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

                try:
                    res = await self.bot.wait_for('button_click', check=check, timeout=20)
                    await res.respond(type=6)
                    embed = discord.Embed(color=0xf5f5f5, title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                                          description=f"You chose **{res.component.label.lower()}**!")
                    await m.edit(embed=embed, components=components)

                    choicelist = ["Heads", "Tails"]
                    choice = random.choice(choicelist)
                    await asyncio.sleep(2)
                    if choice == "Tails":
                        if "Tails" == res.component.label:
                            print("tails - right")
                            embed = discord.Embed(color=0x65DD65, title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                                                  description=f"You chose **{res.component.label.lower()}**!\n\n> **YOU WIN!**")
                            await m.edit(embed=embed, components=tails)
                        if "Heads" == res.component.label:
                            embed = discord.Embed(color=0xed564e, title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                                                  description=f"You chose **{res.component.label.lower()}**!\n\n> You lost.")
                            await m.edit(embed=embed, components=tails)
                    if choice == "Heads":
                        if "Heads" == res.component.label:
                            embed = discord.Embed(color=0x65DD65, title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                                                  description=f"You chose **{res.component.label.lower()}**!\n\n> **YOU WIN!**")
                            await m.edit(embed=embed, components=heads)
                        if "Tails" == res.component.label:
                            embed = discord.Embed(color=0xed564e, title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                                                  description=f"You chose **{res.component.label.lower()}**!\n\n> You lost.")
                            await m.edit(embed=embed, components=heads)

                    res = await self.bot.wait_for('button_click', check=check, timeout=20)
                    await res.respond(type=6)
                    if res.component.label == "Play Again?":
                        await cointoss1(m=m)


                except asyncio.TimeoutError:
                    embed = discord.Embed(color=0xed564e, title="Timeout!", description="No-one reacted. ☹️")
                    await m.edit(embed=embed, components=[
                        Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True)])

        await cointoss1()


def setup(bot):
    DiscordComponents(bot) # Remove this if you already have it in an on_ready event.
    bot.add_cog(calc(bot))
#PythonSerious - 2021
