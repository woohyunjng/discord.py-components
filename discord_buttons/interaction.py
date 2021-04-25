__all__ = ("InteractionType", "FlagsType")


class InteractionType:
    """A class containing interaction types"""

    Pong = 1
    ChannelMessageWithSource = 4
    DeferredChannelMessageWithSource = 5
    IgnoredChannelMessageWithSource = 6


class FlagsType:
    """A class containing flag types"""

    Crossposted = 1 << 0
    Is_crosspost = 1 << 1
    Suppress_embeds = 1 << 2
    Source_message_deleted = 1 << 3
    Urgent = 1 << 4
    Ephemeral = 1 << 6
    Loading = 1 << 7
