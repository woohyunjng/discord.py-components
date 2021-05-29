from discord import User, Client, Embed, AllowedMentions, InvalidArgument
from discord.ext.commands import Bot
from discord.http import Route

from aiohttp import FormData
from typing import Union, List
from json import dumps

from .button import Button
from .message import ComponentMessage
from .interaction import InteractionType, FlagsType
from .component import Component


__all__ = ("Context",)


class Context:
    """Contains information about components interact event.

    Parameters
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        Discord client to use.
    client: :class:`~discord_components.DiscordComponents`
        The client for discord_components.
    user: :class:`discord.User`
        The user interacted with the component.
    component: :class:`~discord_components.Component`
        The interacted component.

        Component json if ephemeral message
    raw_data: :class:`dict`
        JSON sent by discord api.
    message: :class:`~discord_components.ComponentMessage`
        The component's message.
    is_ephemeral: :class:`bool`
        If ephemeral message

    Attributes
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        Discord client to use.
    client: :class:`~discord_components.DiscordComponent`
        The client for discord_components.
    user: :class:`discord.User`
        The user interacted with the component.
    author: :class:`discord.User`
        Alias of `user`
    component: :class:`~discord_components.Component`
        The interacted component.

        Component json if ephemeral message
    raw_data: :class:`dict`
        JSON sent by discord api.
    message: :class:`discord_components.ComponentMessage`
        The component's message.

        None if ephemeral message
    channel: :class:`discord.abc.Messageable`
        The component message's channel.

        None if ephemeral message
    guild: :class:`discord.Guild`
        The component message's guild.

        None if ephemeral message
    interaction_id: :class:`str`
        The interaction's ID.
    interaction_token: :class:`str`
        The interaction's token.
    is_ephemeral: :class:`bool`
        If ephemeral message
    responded: :class:`bool`
        If responded?
    """

    def __init__(
        self, *, bot, client, user=None, component, raw_data, message=None, is_ephemeral=False
    ):
        self.bot = bot
        self.client = client

        self.user = user
        self.author = self.user

        self.component = component
        self.raw_data = raw_data
        self.is_ephemeral = is_ephemeral
        self.responded = False

        self.message = message
        self.channel = message.channel if message else None
        self.guild = message.guild if message else None

        self.interaction_id = raw_data["d"]["id"]
        self.interaction_token = raw_data["d"]["token"]

    async def respond(
        self,
        *,
        type=InteractionType.ChannelMessageWithSource,
        content=None,
        embed=None,
        embeds=[],
        allowed_mentions=None,
        tts=False,
        flags=FlagsType.Ephemeral,
        components=[],
        **options,
    ) -> None:
        """Sends response to Discord.

        .. note::
            If this function is invoked before `wait_for`, a interaction error will be raised.

        :returns: :class:`None`

        Parameters
        ----------
        type: :class:`int`
            The interaction's type. (4 ~ 6)
            Defaults to ``6``. (InteractionType.ChannelMessageWithSource)
        content: Optional[:class:`str`]
            The response message's content.
        embed: Optional[:class:`discord.Embed`]
            The response message's embed.
        embeds: Optional[List[:class:`discord.Embed`]]
            The response message's embeds.
        allowed_mentions: Optional[:class:`discord.AllowedMentions`]
            The response message's allowed mentions.
        tts: Optional[:class:`bool`]
            The response message's tts. (Defaults to ``False``)
        flags: Optional[:class:`int`]
            The response message's flags. (Defaults to ``64``)
        components: List[Union[:class:`~discord_components.Component`, List[:class:`~discord_components.Component`]]]
            The components to send.
            If this is 2-dimensional array, an array is a line
        """
        if self.responded:
            return

        state = self.bot._get_state()
        data = {**self.client._get_components_json(components), **options, "flags": flags}

        if content:
            data["content"] = content

        if embed and embeds:
            embeds.append(embed)
        elif embed:
            embeds = [embed]

        if len(embeds) > 10:
            raise InvalidArgument("Embed limit exceeded. (Max: 10)")
        if embeds:
            embeds = list(map(lambda x: x.to_dict(), embeds))

        if embeds:
            data["embeds"] = embeds

        if allowed_mentions:
            if state.allowed_mentions:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()

            data["allowed_mentions"] = allowed_mentions

        if tts is not None:
            data["tts"] = tts

        self.responded = True
        await self.bot.http.request(
            Route("POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"),
            json={"type": type, "data": data},
        )
