# By @Elektron-blip and @minibox24 with code from https://gist.github.com/minibox24/0025c09ca3941fca541e31429f5bd019
import discord
from discord.ext import commands
from discord.http import Route
from discord_slash import SlashCommand
from discord_components import DiscordComponents, Button, ButtonStyle

client = commands.Bot(command_prefix="-")
slash = SlashCommand(client, sync_commands=True)
DiscordComponents(client)

known_activities = {
    "YouTube": 755600276941176913,
    "Betreyal": 773336526917861400,
    "Fishington": 814288819477020702,
}


@slash.slash(
    name="activities",
    description="Discord activities. They are a lot of fun.",
)
async def _activities(ctx):
    m = await ctx.send(content="<a:typing:597589448607399949> Neo Bot is thinking...")
    components = []
    for k, _i in known_activities.items():
        components.append(Button(style=ButtonStyle.blue, label=k))
    await m.edit(
        content="Here are your choices.",
        components=components,
    )
    res = await client.wait_for("button_click", timeout=60)
    if not res:
        await ctx.channel.send("Too Late")
    elif res.author.id == ctx.author.id:
        voice = ctx.author.voice

        if not voice:
            return await res.respond(
                content="You have to be in a voice channel to use this command.", type=7
            )

        r = Route("POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id)

        payload = {
            "max_age": 60,
            "target_type": 2,
            "target_application_id": known_activities[res.component.label],
        }

        try:
            code = (await client.http.request(r, json=payload))["code"]
        except discord.Forbidden:

            return await res.respond(
                content="I Need the `Create Invite` permission.", type=7
            )

        await res.respond(
            embed=discord.Embed(
                description=f"[Click here!](https://discord.gg/{code})\nLink expires in 1 minute",
                color=discord.Colour.red(),
            ),
            type=7,
        )
    else:
        await res.respond(type=6)


client.run("YOUR_TOKEN")
