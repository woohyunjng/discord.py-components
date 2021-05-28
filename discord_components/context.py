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
    raw_data: :class:`dict`
        JSON sent by discord api.
    message: :class:`~discord_components.ComponentMessage`
        The component's message.

    Attributes
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        Discord client to use.
    client: :class:`~discord_components.DiscordComponent`
        The client for discord_components.
    user: :class:`discord.User`
        The user interacted with the component.
    component: :class:`~discord_components.Component`
        The interacted component.
    raw_data: :class:`dict`
        JSON sent by discord api.
    message: :class:`discord_components.ComponentMessage`
        The component's message.
    channel: :class:`discord.abc.Messageable`
        The component message's channel.
    guild: :class:`discord.Guild`
        The component message's guild.
    interaction_id: :class:`str`
        The interaction's ID.
    interaction_token: :class:`str`
        The interaction's token.
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
    ) -> None:
        """Sends response to Discord.

        .. note::
            If this function is invoked before `wait_for_button_click`, a interaction error will be raised.

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
        """
        state = self.bot._get_state()

        if embed and embeds:
            embeds.append(embed)
        elif embed:
            embeds = [embed]

        if len(embeds) > 10:
            raise InvalidArgument("Embed limit exceeded. (Max: 10)")
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
            "allowed_mentions": allowed_mentions,
            "tts": tts,
            "flags": flags,
        }

        await self.bot.http.request(
            Route("POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"),
            json={"type": type, "data": data},
        )
