from typing import Optional, List, Union

from discord import (
    Message,
    Embed,
    Attachment,
    AllowedMentions,
    InvalidArgument,
    File,
    MessageFlags,
)
from discord.http import Route, HTTPClient
from discord.abc import Messageable, Snowflake
from discord.ext.commands import Context

from .utils import _get_components_json, _form_files
from .component import _get_component_type, ActionRow, Component

__all__ = ("ComponentMessage",)


class ComponentMessage(Message):
    __slots__ = tuple(list(Message.__slots__) + ["components", "ephemeral"])

    def __init__(self, *, state, channel, data, ephemeral=False):
        super().__init__(state=state, channel=channel, data=data)
        self.ephemeral = ephemeral

        components = []
        for i in data["components"]:
            components.append(ActionRow())
            for j in i["components"]:
                components[-1].append(_get_component_type(j["type"]).from_json(j))
        self.components: List[ActionRow] = components

    def get_component(self, custom_id: str) -> Optional[Component]:
        for row in self.components:
            for component in row.components:
                if component.custom_id == custom_id:
                    return component

    async def edit(
        self,
        content: Optional[str] = None,
        embed: Optional[Embed] = None,
        embeds: List[Embed] = None,
        suppress: bool = None,
        attachments: List[Attachment] = None,
        delete_after: Optional[float] = None,
        allowed_mentions: Optional[AllowedMentions] = None,
        components: List[Union[ActionRow, Component, List[Component]]] = None,
        **fields,
    ):
        if self.ephemeral:
            return

        state = self._state
        data = {}

        if content is not None:
            data["content"] = content

        if embed is not None and embeds is not None:
            raise InvalidArgument(
                "cannot pass both embed and embeds parameter to edit()"
            )

        if embed is not None:
            data["embeds"] = [embed.to_dict()]

        if embeds is not None:
            data["embeds"] = [e.to_dict() for e in embeds]

        if suppress is not None:
            flags = MessageFlags._from_value(0)
            flags.suppress_embeds = True
            data["flags"] = flags.value

        if allowed_mentions is None:
            if (
                state.allowed_mentions is not None
                and self.author.id == self._state.self_id
            ):
                data["allowed_mentions"] = state.allowed_mentions.to_dict()
        else:
            if state.allowed_mentions is not None:
                data["allowed_mentions"] = state.allowed_mentions.merge(
                    allowed_mentions
                ).to_dict()
            else:
                data["allowed_mentions"] = allowed_mentions.to_dict()

        if attachments is not None:
            data["attachments"] = [a.to_dict() for a in attachments]

        if components is not None:
            data["components"] = _get_components_json(components)

        if data:
            await state.http.request(
                Route(
                    "PATCH",
                    "/channels/{channel_id}/messages/{message_id}",
                    channel_id=self.channel.id,
                    message_id=self.id,
                ),
                json=data,
            )

        if delete_after is not None:
            await self.delete(delay=delete_after)

    async def delete(self, *args, **kwargs):
        if self.ephemeral:
            return

        return await super().delete(*args, **kwargs)


def new_override(cls, *args, **kwargs):
    if isinstance(cls, Message):
        return object.__new__(ComponentMessage)
    else:
        return object.__new__(cls)


Message.__new__ = new_override


def send_files(
    self,
    channel_id: Snowflake,
    *,
    files,
    content=None,
    tts=False,
    embed=None,
    embeds=None,
    stickers=None,
    nonce=None,
    allowed_mentions=None,
    message_reference=None,
    components=None,
):
    data = {"tts": tts}
    if content is not None:
        data["content"] = content
    if embed is not None:
        data["embeds"] = [embed]
    if embeds is not None:
        data["embeds"] = embeds
    if nonce is not None:
        data["nonce"] = nonce
    if allowed_mentions is not None:
        data["allowed_mentions"] = allowed_mentions
    if message_reference is not None:
        data["message_reference"] = message_reference
    if stickers is not None:
        data["sticker_ids"] = stickers
    if components is not None:
        data["components"] = components

    form = _form_files(data, files, use_form=False)
    return self.request(
        Route("POST", "/channels/{channel_id}/messages", channel_id=channel_id),
        form=form,
        files=files,
    )


def send_message(
    self,
    channel_id,
    content,
    *,
    tts=False,
    embed=None,
    embeds=None,
    nonce=None,
    allowed_mentions=None,
    message_reference=None,
    stickers=None,
    components=None,
):
    payload = {"tts": tts}

    if content is not None:
        payload["content"] = content

    if embed is not None:
        payload["embeds"] = [embed]

    if embeds is not None:
        payload["embeds"] = embeds

    if nonce is not None:
        payload["nonce"] = nonce

    if allowed_mentions is not None:
        payload["allowed_mentions"] = allowed_mentions

    if message_reference is not None:
        payload["message_reference"] = message_reference

    if stickers is not None:
        payload["sticker_ids"] = stickers

    if components is not None:
        payload["components"] = components

    return self.request(
        Route("POST", "/channels/{channel_id}/messages", channel_id=channel_id),
        json=payload,
    )


HTTPClient.send_files = send_files
HTTPClient.send_message = send_message


async def send(
    self,
    content=None,
    *,
    tts=False,
    embed=None,
    embeds=None,
    file=None,
    files=None,
    stickers=None,
    delete_after=None,
    nonce=None,
    allowed_mentions=None,
    reference=None,
    mention_author=None,
    components=None,
):
    state = self._state
    channel = await self._get_channel()
    content = str(content) if content is not None else None

    if embed is not None and embeds is not None:
        raise InvalidArgument("cannot pass both embed and embeds parameter to send()")

    if embed is not None:
        embeds = [embed.to_dict()]

    elif embeds is not None:
        if len(embeds) > 10:
            raise InvalidArgument(
                "embeds parameter must be a list of up to 10 elements"
            )
        embeds = [embed.to_dict() for embed in embeds]

    if stickers is not None:
        stickers = [sticker.id for sticker in stickers]

    if allowed_mentions is not None:
        if state.allowed_mentions is not None:
            allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
        else:
            allowed_mentions = allowed_mentions.to_dict()
    else:
        allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()

    if mention_author is not None:
        allowed_mentions = allowed_mentions or AllowedMentions().to_dict()
        allowed_mentions["replied_user"] = bool(mention_author)

    if reference is not None:
        try:
            reference = reference.to_message_reference_dict()
        except AttributeError:
            raise InvalidArgument(
                "reference parameter must be Message or MessageReference"
            ) from None

    if components is not None:
        components = _get_components_json(components)

    if file is not None and files is not None:
        raise InvalidArgument("cannot pass both file and files parameter to send()")

    if file is not None:
        if not isinstance(file, File):
            raise InvalidArgument("file parameter must be File")

        try:
            data = await state.http.send_files(
                channel.id,
                files=[file],
                allowed_mentions=allowed_mentions,
                content=content,
                tts=tts,
                embed=embed,
                embeds=embeds,
                nonce=nonce,
                message_reference=reference,
                stickers=stickers,
                components=components,
            )
        finally:
            file.close()

    elif files is not None:
        if len(files) > 10:
            raise InvalidArgument("files parameter must be a list of up to 10 elements")
        elif not all(isinstance(file, File) for file in files):
            raise InvalidArgument("files parameter must be a list of File")

        try:
            data = await state.http.send_files(
                channel.id,
                files=files,
                content=content,
                tts=tts,
                embed=embed,
                embeds=embeds,
                nonce=nonce,
                allowed_mentions=allowed_mentions,
                message_reference=reference,
                stickers=stickers,
                components=components,
            )
        finally:
            for f in files:
                f.close()
    else:
        data = await state.http.send_message(
            channel.id,
            content,
            tts=tts,
            embed=embed,
            embeds=embeds,
            nonce=nonce,
            allowed_mentions=allowed_mentions,
            message_reference=reference,
            stickers=stickers,
            components=components,
        )

    ret = ComponentMessage(state=state, channel=channel, data=data)
    if delete_after is not None:
        await ret.delete(delay=delete_after)
    return ret


async def send_override(context_or_channel, *args, **kwargs):
    if isinstance(context_or_channel, Context):
        channel = context_or_channel.channel
    else:
        channel = context_or_channel

    return await send(channel, *args, **kwargs)


async def fetch_message(context_or_channel, id: int):
    if isinstance(context_or_channel, Context):
        channel = context_or_channel.channel
    else:
        channel = context_or_channel

    state = channel._state
    data = await state.http.get_message(channel.id, id)
    return ComponentMessage(state=state, channel=channel, data=data)


Messageable.send = send_override
Messageable.fetch_message = fetch_message
