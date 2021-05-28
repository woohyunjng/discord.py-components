from discord import User, Client, Embed, AllowedMentions, InvalidArgument
from discord.ext.commands import Bot
from discord.http import Route

from .button import Button
from .message import ComponentMessage
from .interaction import InteractionType, FlagsType
from .component import Component

from typing import Union, List


__all__ = ("Context",)


class Context:
    """A class which contains a lot of information about components interact event

    Parameters
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The bot
    client: :class:`~discord_components.DiscordComponents`
        The client for discord_components
    user: :class:`discord.User`
        The user which interacted with the component
    component: :class:`~discord_components.Component`
        The component which was interacted
    raw_data: :class:`dict`
        JSON which was sent by discord api
    message: :class:`~discord_components.ComponentMessage`
        The component's message

    Attributes
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The bot
    client: :class:`~discord_components.DiscordComponent`
        The client for discord_components
    user: :class:`discord.User`
        The user which interacted with the component
    component: :class:`~discord_components.Component`
        The component which was interacted
    raw_data: :class:`dict`
        JSON which was sent by discord api
    message: :class:`discord_components.ComponentMessage`
        The component's message
    channel: :class:`discord.abc.Messageable`
        The component's message's channel
    guild: :class:`discord.Guild`
        The component's message's guild
    interaction_id: :class:`str`
        The interaction's id
    interaction_token: :class:`str`
        The interaction's token
    """

    def __init__(
        self,
        *,
        bot,
        client,
        user,
        component,
        raw_data,
        message,
    ):
        self.bot = bot
        self.client = client
        self.user = user

        self.component = component
        self.raw_data = raw_data

        self.message = message
        self.channel = message.channel
        self.guild = message.guild

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
    ) -> None:
        """Function to send response to discord

        .. note::
            If you don't use this function after using `wait_for_button_click`, a interaction error will be raised

        :returns: :class:`None`

        Parameters
        ----------
        type: :class:`int`
            The interaction's type. (4 or more and 6 or less)
            Default 6 (InteractionType.ChannelMessageWithSource)
        content: Optional[:class:`str`]
            The response message's content
        embed: Optional[:class:`discord.Embed`]
            The response message's embed
        embeds: Optional[List[:class:`discord.Embed`]]
            The response message's embeds
        allowed_mentions: Optional[:class:`discord.AllowedMentions`]
            The response message's allowed mentions
        tts: Optional[:class:`bool`]
            The response message's tts (default False)
        flags: Optional[:class:`int`]
            The response message's flags (default 64)
        components: List[Union[:class:`~discord_components.Component`, List[:class:`~discord_components.Component`]]]
            The components to send.
            If this is 2-dimensional array, an array is a line
        """
        state = self.bot._get_state()

        if embed and embeds:
            embeds.append(embed)
        elif embed:
            embeds = [embed]

        if len(embeds) > 10:
            raise InvalidArgument("Do not provide more than 10 embeds")
        if embeds:
            embeds = list(map(lambda x: x.to_dict(), embeds))

        if allowed_mentions:
            if state.allowed_mentions:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()

        data = {
            "content": content,
            "embeds": embeds,
            **self.client._get_components_json(components),
            "allowed_mentions": allowed_mentions,
            "tts": tts,
            "flags": flags,
        }

        await self.bot.http.request(
            Route("POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"),
            json={"type": type, "data": data},
        )
