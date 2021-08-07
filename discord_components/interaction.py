from typing import List, Union, Optional

from discord import (
    User,
    Embed,
    AllowedMentions,
    InvalidArgument,
    Guild,
    NotFound,
    Member,
    Object,
    MessageFlags,
)
from discord.state import ConnectionState
from discord.abc import Messageable
from discord.http import Route

from enum import IntEnum

from .utils import _get_components_json
from .component import Component, ActionRow, Button, Select
from .dpy_overrides import ComponentMessage


__all__ = ("Interaction", "InteractionEventType")


class InteractionEventType(IntEnum):
    button_click = 2
    select_option = 3


class Interaction:
    def __init__(
        self,
        *,
        state: ConnectionState,
        client: "DiscordComponents",
        raw_data: dict,
    ):
        self.state: ConnectionState = state
        self.client: "DiscordComponents" = client

        self.interaction_id: int = int(raw_data["id"])
        self.interaction_token: str = raw_data["token"]

        self.custom_id: str = raw_data["data"]["custom_id"]
        self.values: List[str] = raw_data["data"].get("values", [])
        self.component_type: int = raw_data["data"]["component_type"]

        self.channel_id: int = int(raw_data["channel_id"])
        self.guild_id: int = int(raw_data["guild_id"])

        if self.guild:
            self.user: Union[User, Member] = Member(
                state=state, guild=self.guild, data=raw_data["member"]
            )
        elif self.raw_data.get("member"):
            self.user: Union[User, Member] = User(
                state=state, data=raw_data["member"]["user"]
            )
        else:
            self.user: Union[User, Member] = User(state=state, data=raw_data["user"])
        self.author: Union[User, Member] = self.user

        if raw_data["message"].get("components"):
            self.message: Union[ComponentMessage, dict] = ComponentMessage(
                state=state, channel=self.channel, data=raw_data["message"]
            )
            self.component: Component = self.message.get_component(
                custom_id=self.custom_id
            )
        else:
            self.message: Union[ComponentMessage, dict] = raw_data["message"]

            if self.component_type == 2:
                self.component: Component = Button.from_json(raw_data["data"])
            elif self.component_type == 3:
                self.component: Component = Select.from_json(raw_data["data"])

        self.raw_data: dict = raw_data
        self.responded: bool = False
        self.deferred: bool = False

        self._deferred_hidden = False
        self._deferred_edit_origin = False

    @property
    def channel(self) -> Optional[Messageable]:
        return self.state.get_channel(self.channel_id)

    @property
    def guild(self) -> Optional[Guild]:
        return self.state._get_guild(self.guild_id)

    async def defer(self, ephemeral: bool = True, edit_origin: bool = False):
        if self.deferred or self.responded:
            return

        await self.respond(type=5 if not edit_origin else 6, ephemeral=ephemeral)

        if ephemeral:
            self._deferred_hidden = True
        self._deferred_edit_origin = edit_origin

    async def respond(
        self,
        *,
        type: int = 4,
        content: str = None,
        embed: Embed = None,
        embeds: List[Embed] = None,
        suppress: bool = None,
        allowed_mentions: AllowedMentions = None,
        tts: bool = False,
        ephemeral: bool = True,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
    ) -> Optional[Union[ComponentMessage, dict]]:
        state = self.state
        data = {"tts": tts}

        if ephemeral:
            data["flags"] = 64

        if content is not None:
            data["content"] = str(content)

        if embed is not None and embeds is not None:
            raise InvalidArgument("cannot pass both embed and embeds parameter")

        if embed is not None:
            data["embeds"] = [embed.to_dict()]

        if embeds is not None:
            if len(embeds) > 10:
                raise InvalidArgument(
                    "embeds parameter must be a list of up to 10 elements"
                )
            data["embeds"] = [embed.to_dict() for embed in embeds]

        if suppress is not None:
            flags = MessageFlags._from_value(
                self.message.flags if isinstance(self.message, ComponentMessage) else 0
            )
            flags.suppress_embeds = suppress
            data["flags"] = flags.value

        if allowed_mentions is not None:
            if state.allowed_mentions is not None:
                data["allowed_mentions"] = state.allowed_mentions.merge(
                    allowed_mentions
                ).to_dict()
            else:
                data["allowed_mentions"] = allowed_mentions.to_dict()
        else:
            data["allowed_mentions"] = (
                state.allowed_mentions and state.allowed_mentions.to_dict()
            )

        if components is not None:
            data["components"] = _get_components_json(components)

        try:
            if self.deferred:
                res = await self.state.http.request(
                    Route(
                        "PATCH",
                        f"/webhooks/{self.state.self_id}/{self.interaction_token}/messages/@original",
                    ),
                    json=data,
                )
            else:
                res = await self.state.http.request(
                    Route(
                        "POST",
                        f"/interactions/{self.interaction_id}/{self.interaction_token}/callback",
                    ),
                    json={"type": type, "data": data},
                )

            if type in (4, 7):
                self.responded = True
            else:
                self.deferred = True
        except NotFound as e:
            raise NotFound(
                e.response,
                "Interaction is unknown (you have already responded to the interaction or responding took too long)",
            ) from None

        if not ephemeral and type in (4, 7):
            return ComponentMessage(
                state=state,
                data=res,
                channel=self.channel or Object(id=self.channel_id),
            )
        else:
            return res

    async def send(
        self,
        content: str = None,
        embed: Embed = None,
        embeds: List[Embed] = None,
        allowed_mentions: AllowedMentions = None,
        tts: bool = False,
        ephemeral: bool = True,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
        delete_after: float = None,
    ) -> Optional[Union[ComponentMessage, dict]]:
        res = await self.respond(
            type=4,
            content=content,
            embed=embed,
            embeds=embeds,
            allowed_mentions=allowed_mentions,
            tts=tts,
            ephemeral=ephemeral,
            components=components,
        )
        if isinstance(res, dict):
            return res
        elif res is not None and delete_after is not None:
            await res.delete(delay=delete_after)

    async def edit_origin(
        self,
        content: str = None,
        embed: Embed = None,
        embeds: List[Embed] = None,
        suppress: bool = None,
        allowed_mentions: AllowedMentions = None,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
        delete_after: float = None,
    ):
        res = await self.respond(
            type=7,
            content=content,
            embed=embed,
            embeds=embeds,
            suppress=suppress,
            allowed_mentions=allowed_mentions,
            components=components,
        )
        if isinstance(res, dict):
            return res
        elif res is not None and delete_after is not None:
            await res.delete(delay=delete_after)
