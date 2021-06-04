"""
@PythonSerious - 2021
https://github.com/PythonSerious
"""
import discord
from discord.ext.commands import command, Cog
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio


class PascalCase(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command()
    async def tictactoe(self, ctx, member: discord.Member):
        if ctx.author == member:
            return await ctx.send("You can't play against yourself!")
        embed = discord.Embed(color=0xF5F5F5, title=f"Hey, {ctx.author.name} wants to play tic-tac-toe with you!")
        acceptdenycomps = [
            [
                Button(style=ButtonStyle.green, label="Accept"),
                Button(style=ButtonStyle.red, label="Decline")
            ]
        ]
        #
        board = [
            [
                Button(style=ButtonStyle.grey, label="⠀", id="0 0"),
                Button(style=ButtonStyle.grey, label="⠀", id="0 1"),
                Button(style=ButtonStyle.grey, label="⠀", id="0 2")

            ],
            [
                Button(style=ButtonStyle.grey, label="⠀", id="1 0"),
                Button(style=ButtonStyle.grey, label="⠀", id="1 1"),
                Button(style=ButtonStyle.grey, label="⠀", id="1 2")

            ],
            [
                Button(style=ButtonStyle.grey, label="⠀", id="2 0"),
                Button(style=ButtonStyle.grey, label="⠀", id="2 1"),
                Button(style=ButtonStyle.grey, label="⠀", id="2 2")
            ]
        ]
        selections = [
            [
                "unchosen",
                "unchosen",
                "unchosen"
            ],
            [
                "unchosen",
                "unchosen",
                "unchosen"
            ],
            [
                "unchosen",
                "unchosen",
                "unchosen"
            ]
        ]
        
        m = await ctx.send(embed=embed, components=acceptdenycomps, content=member.mention)
        def haswon(team):
            if selections[0][0] == team and selections[0][1] == team and selections[0][2] == team:
                return True
            if selections[1][0] == team and selections[1][1] == team and selections[1][2] == team:
                return True
            if selections[2][0] == team and selections[2][1] == team and selections[2][2] == team:
                return True
            if selections[0][0] == team and selections[1][0] == team and selections[2][0] == team:
                return True
            if selections[0][1] == team and selections[1][1] == team and selections[2][1] == team:
                return True
            if selections[0][2] == team and selections[1][2] == team and selections[2][2] == team:
                return True
            if selections[0][0] == team and selections[1][1] == team and selections[2][2] == team:
                return True
            if selections[0][2] == team and selections[1][1] == team and selections[2][0] == team:
                return True
            else:
                return False
        def istie(team):
            if not "unchosen" in str(selections):
                if not haswon(team):

                    return True
                else:

                    return False
            else:

                return False


        def confirmcheck(res):
            return res.user.id == member.id and res.channel.id == ctx.channel.id and str(res.message.id) == str(m.id)

        try:
            res = await self.bot.wait_for("button_click", check=confirmcheck, timeout=50)
        except asyncio.TimeoutError:
            await msg.edit(
                embed=Embed(color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"),
                components=[
                    Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True),
                    Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/PythonSerious")
                ],
            )
            return
        await res.respond(type=6)
        if res.component.label == "Accept":
            accept = True
            embed = discord.Embed(color=discord.Colour.green(), title=f'{member.name} has accepted!', description="The game will now begin...")
            await m.edit(embed=embed)
            await asyncio.sleep(1)

        else:
            accept = False
            embed = discord.Embed(color=discord.Colour.red(), title=f'{member.name} has declined.')
            await m.edit(embed=embed)
            return
        
        async def winner(team):
            if team == "red":
                color = discord.Colour.red()
                user = member
            if team == "green":
                color = discord.Colour.green()
                user = ctx.author
            e = discord.Embed(color=color, title=f"{user.name} has won!")
            board.append(Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/PythonSerious"))
            await m.edit(embed=e, components=board)
            return

            
        
        greensturnembed = discord.Embed(color=0xF5F5F5, title=f"{ctx.author.name}'s turn")
        redsturnembed = discord.Embed(color=0xF5F5F5, title=f"{member.name}'s turn")
        greenstatus = True
        # True = green False = red
        def greensturncheck(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id and res.message.id == m.id
        def redsturncheck(res):
            return res.user.id == member.id and res.channel.id == ctx.channel.id and res.message.id == m.id
        while accept:
            if greenstatus:
                await m.edit(embed=greensturnembed, components=board)
                try:
                    res = await self.bot.wait_for("button_click", check=greensturncheck, timeout=50)
                    await res.respond(type=6)
                    listid = res.component.id
                    firstpart, secondpart = listid.split(' ')
                    board[int(firstpart)][int(secondpart)] = Button(style=ButtonStyle.green, label="⠀", id="1 0", disabled=True)
                    selections[int(firstpart)][int(secondpart)] = "green"
                    if haswon('green'):
                        await winner('green')
                        accept = False
                        return
                    if istie('green'):
                        e = discord.Embed(color=0xF5F5F5, title=f"Call it a tie!")
                        board.append(Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/PythonSerious"))
                        await m.edit(embed=e, components=board)
                        accept = False
                        return
                    greenstatus = False
                    pass
                    

                except asyncio.TimeoutError:
                    await msg.edit(
                        embed=Embed(color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"),
                        components=[
                            Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True),
                            Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/PythonSerious")
                        ],
                    )
                    return
            if not greenstatus:
                await m.edit(embed=redsturnembed, components=board)
                try:
                    res = await self.bot.wait_for("button_click", check=redsturncheck, timeout=50)
                    await res.respond(type=6)
                    listid = res.component.id
                    firstpart, secondpart = listid.split(' ')
                    board[int(firstpart)][int(secondpart)] = Button(style=ButtonStyle.red, label="⠀", id="1 0",
                                                                 disabled=True)
                    selections[int(firstpart)][int(secondpart)] = "red"
                    if haswon('red'):
                        await winner('red')
                        accept = False
                        return
                    if istie('red'):
                        e = discord.Embed(color=0xF5F5F5, title=f"Call it a tie!")
                        board.append(Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/PythonSerious"))
                        await m.edit(embed=e, components=board)
                        accept = False
                        return
                        
                    greenstatus = True
                    pass


                except asyncio.TimeoutError:
                    await msg.edit(
                        embed=Embed(color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"),
                        components=[
                            Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True),
                            Button(style=ButtonStyle.URL, label="View creator", url="https://github.com/PythonSerious")
                        ],
                    )
                    return





def setup(bot):
    print('Tictactoe - by python#0001 has loaded!')
    DiscordComponents(bot)  #if you have this in an on_ready event you can remove this line.
    bot.add_cog(PascalCase(bot))
