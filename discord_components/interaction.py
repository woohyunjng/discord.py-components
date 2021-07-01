from discord import User, Client, Embed, AllowedMentions, InvalidArgument, Message, Guild, NotFound
from discord.abc import Messageable
from discord.ext.commands import Bot
from discord.http import Route

from typing import List, Union

from .component import Component, ActionRow


__all__ = ("Interaction", "InteractionType", "InteractionEventType")


InteractionEventType = {"button_click": 2, "select_option": 3}


class InteractionType:
    Pong: int = 1
    ChannelMessageWithSource: int = 4
    DeferredChannelMessageWithSource: int = 5
    DeferredUpdateMessage: int = 6
    UpdateMessage: int = 7


class Interaction:
    def __init__(
        self,
        *,
        bot: Union[Client, Bot],
        client: "DiscordComponents",
        user: User,
        channel: Messageable,
        guild: Guild,
        parent_component: Component,
        interacted_component: Component,
        raw_data: dict,
        message: Message,
        is_ephemeral: bool = False,
    ):
        self.bot = bot
        self.client = client

        self.user = user
        self.author = self.user

        self.component = interacted_component
        self.interacted_component = self.component
        self.parent_component = parent_component

        self.raw_data = raw_data
        self.is_ephemeral = is_ephemeral
        self.responded = False

        self.message = message
        self.channel = channel
        self.guild = guild

        self.interaction_id = raw_data["d"]["id"]
        self.interaction_token = raw_data["d"]["token"]

        self.custom_id = raw_data["d"]["data"]["custom_id"]

    async def respond(
        self,
        *,
        type: int = InteractionType.ChannelMessageWithSource,
        content: str = None,
        embed: Embed = None,
        embeds: List[Embed] = None,
        allowed_mentions: AllowedMentions = None,
        tts: bool = False,
        ephemeral: bool = True,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
        **options,
    ) -> None:
        state = self.bot._get_state()
        data = {
            **self.client._get_components_json(components),
            **options,
            "flags": 64 if ephemeral else 0,
        }

        if content is not None:
            data["content"] = content

        if embed and embeds:
            embeds.append(embed)
        elif embed:
            embeds = [embed]

        if embeds:
            embeds = list(map(lambda x: x.to_dict(), embeds))
            if len(embeds) > 10:
                raise InvalidArgument("Embed limit exceeded. (Max: 10)")
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
        try:
            await self.bot.http.request(
                Route(
                    "POST", f"/interactions/{self.interaction_id}/{self.interaction_token}/callback"
                ),
                json={"type": type, "data": data},
            )
        except NotFound as e:
            raise NotFound(
                e.response,
                "Interaction is unknown (you have already responded to the interaction or responding took too long)",
            ) from None
