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
    File,
)
from discord.state import ConnectionState
from discord.abc import Messageable

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
        self.guild_id: int = raw_data.get("guild_id")
        if self.guild_id is not None:
            self.guild_id = int(self.guild_id)

        if self.guild:
            self.user: Union[User, Member] = Member(
                state=state, guild=self.guild, data=raw_data["member"]
            )
        elif raw_data.get("member"):
            self.user: Union[User, Member] = User(state=state, data=raw_data["member"]["user"])
        else:
            self.user: Union[User, Member] = User(state=state, data=raw_data["user"])
        self.author: Union[User, Member] = self.user

        self.message: Union[ComponentMessage, dict] = ComponentMessage(
            state=state,
            channel=self.channel,
            data=raw_data["message"],
            ephemeral=raw_data["message"].get("flags") == 64,
        )
        self.component: Component = self.message.get_component(custom_id=self.custom_id)

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
        file: File = None,
        files: List[File] = None,
        allowed_mentions: AllowedMentions = None,
        tts: bool = False,
        ephemeral: bool = True,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
    ) -> Optional[Union[ComponentMessage, dict]]:
        if self.responded:
            return

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
                raise InvalidArgument("embeds parameter must be a list of up to 10 elements")
            data["embeds"] = [embed.to_dict() for embed in embeds]

        if suppress is not None:
            flags = MessageFlags._from_value(
                self.message.flags if isinstance(self.message, ComponentMessage) else 0
            )
            flags.suppress_embeds = suppress
            data["flags"] = flags.value

        if allowed_mentions is not None:
            if state.allowed_mentions is not None:
                data["allowed_mentions"] = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                data["allowed_mentions"] = allowed_mentions.to_dict()
        else:
            data["allowed_mentions"] = state.allowed_mentions and state.allowed_mentions.to_dict()

        if components is not None:
            data["components"] = _get_components_json(components)

        if not self.deferred:
            data = {"type": type, "data": data}

        if file is not None and files is not None:
            raise InvalidArgument("cannot pass both file and files parameter to send()")
        elif files is not None:
            if len(files) > 10:
                raise InvalidArgument("files parameter must be a list of up to 10 elements")
        if file is not None:
            files = [file]

        try:
            if self.deferred:
                res = await self.client.http.edit_response(
                    interaction_token=self.interaction_token, data=data, files=files
                )
            else:
                res = await self.client.http.initial_response(
                    interaction_id=self.interaction_id,
                    interaction_token=self.interaction_token,
                    data=data,
                    files=files,
                )

            if type in (4, 7):
                self.responded = True
            else:
                self.deferred = True
        except NotFound as e:
            self.responded = True
            raise NotFound(
                e.response,
                "Interaction is unknown (you have already responded to the interaction or responding took too long)",
            ) from None

        if type in (4, 7) and isinstance(res, dict):
            return ComponentMessage(
                state=state,
                data=res,
                channel=self.channel or Object(id=self.channel_id),
                ephemeral=res.get("flags") == 64,
            )
        else:
            return res

    async def send(
        self,
        content: str = None,
        embed: Embed = None,
        embeds: List[Embed] = None,
        file: File = None,
        files: List[File] = None,
        allowed_mentions: AllowedMentions = None,
        tts: bool = False,
        ephemeral: bool = True,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
        delete_after: float = None,
    ) -> Optional[Union[ComponentMessage, dict]]:
        await self.defer(ephemeral=ephemeral)
        res = await self.respond(
            type=4,
            content=content,
            embed=embed,
            embeds=embeds,
            file=file,
            files=files,
            allowed_mentions=allowed_mentions,
            tts=tts,
            ephemeral=ephemeral,
            components=components,
        )

        if delete_after is None:
            return res
        elif res is not None:
            await res.delete(delay=delete_after)

    async def edit_origin(
        self,
        content: str = None,
        embed: Embed = None,
        embeds: List[Embed] = None,
        suppress: bool = None,
        file: File = None,
        files: List[File] = None,
        allowed_mentions: AllowedMentions = None,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
        delete_after: float = None,
    ):
        await self.defer(edit_origin=True)
        res = await self.respond(
            type=7,
            content=content,
            embed=embed,
            embeds=embeds,
            suppress=suppress,
            file=file,
            files=files,
            allowed_mentions=allowed_mentions,
            components=components,
        )

        if delete_after is None:
            return res
        elif res is not None:
            await res.delete(delay=delete_after)
