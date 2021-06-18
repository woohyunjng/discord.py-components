from discord import Message, Guild, TextChannel, User

from discord_components.interaction import Interaction
from discord_components.component import Component


__all__ = ("message_filter", "component_filter", "guild_filter", "channel_filter", "user_filter")


def message_filter(message: Message, ephemeral: bool = False):
    def filter(interaction: Interaction):
        if ephemeral or isinstance(interaction.message, dict):
            return False

        return interaction.message.id == message.id

    return filter


def component_filter(component: Component):
    def filter(interaction: Interaction):
        return interaction.component.id == component.id

    return filter


def guild_filter(guild: Guild):
    def filter(interaction: Interaction):
        return interaction.guild.id == guild.id

    return filter


def channel_filter(channel: TextChannel):
    def filter(interaction: Interaction):
        return interaction.channel.id == channel.id

    return filter


def user_filter(user: User):
    def filter(interaction: Interaction):
        return interaction.user.id == user.id

    return filter
