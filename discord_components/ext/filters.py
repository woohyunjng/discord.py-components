from discord import Message, Guild, TextChannel, User

from discord_components.interaction import Interaction
from discord_components.component import Component, Button, SelectOption


__all__ = (
    "message_filter",
    "component_filter",
    "guild_filter",
    "channel_filter",
    "user_filter",
)


def message_filter(message: Message, ephemeral: bool = False):
    def _filter(interaction: Interaction):
        if ephemeral or isinstance(interaction.message, dict):
            return False

        return interaction.message.id == message.id

    return _filter


def component_filter(component: Component):
    def _filter(interaction: Interaction):
        return interaction.custom_id == component.id

    return _filter


def guild_filter(guild: Guild):
    def _filter(interaction: Interaction):
        return interaction.guild_id == guild.id

    return _filter


def channel_filter(channel: TextChannel):
    def _filter(interaction: Interaction):
        return interaction.channel_id == channel.id

    return _filter


def user_filter(user: User):
    def _filter(interaction: Interaction):
        return interaction.user.id == user.id

    return _filter
