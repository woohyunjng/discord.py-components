from discord import (
    Client,
    TextChannel,
    Message,
    Embed,
    AllowedMentions,
    InvalidArgument,
    User,
    File,
)
from discord.ext.commands import Bot, Context as DContext
from discord.http import Route
from discord.abc import Messageable

from functools import wraps
from aiohttp import FormData
from asyncio import TimeoutError
from typing import List, Callable, Awaitable, Union
from json import dumps

from .button import Button
from .select import Select
from .component import Component
from .message import ComponentMessage
from .interaction import Interaction, InteractionEventType


__all__ = ("DiscordComponents",)


class DiscordComponents:
    def __init__(
        self,
        bot: Union[Bot, Client],
        change_discord_methods: bool = True,
        add_listener: bool = True,
    ):
        self.bot = bot

        if change_discord_methods:
            self.change_discord_methods(add_listener=add_listener)

    def change_discord_methods(self, add_listener: bool = True):
        async def send_component_msg_prop(ctxorchannel, *args, **kwargs) -> Message:
            if isinstance(ctxorchannel, DContext):
                return await self.send_component_msg(ctxorchannel.channel, *args, **kwargs)
            else:
                return await self.send_component_msg(ctxorchannel, *args, **kwargs)

        async def edit_component_msg_prop(*args, **kwargs):
            return await self.edit_component_msg(*args, **kwargs)

        async def reply_component_msg_prop(msg, *args, **kwargs):
            return await self.send_component_msg(msg.channel, *args, **kwargs, reference=msg)

        async def on_socket_response(res):
            if (res["t"] != "INTERACTION_CREATE") or (res["d"]["type"] != 3):
                return

            ctx = self._get_interaction(res)
            for key, value in InteractionEventType.items():
                if value == res["d"]["data"]["component_type"]:
                    self.bot.dispatch(key, ctx)
                    break

        if isinstance(self.bot, Bot) and add_listener:
            self.bot.add_listener(on_socket_response, name="on_socket_response")
        else:
            self.bot.on_socket_response = on_socket_response

        Messageable.send = send_component_msg_prop
        Message.edit = edit_component_msg_prop
        Message.reply = reply_component_msg_prop

    async def send_component_msg(
        self,
        channel: Messageable,
        content: str = "",
        *,
        tts: bool = False,
        embed: Embed = None,
        file: File = None,
        files: List[File] = None,
        mention_author: bool = None,
        allowed_mentions: AllowedMentions = None,
        reference: Message = None,
        components: List[Union[Component, List[Component]]] = None,
        delete_after: float = None,
        **options,
    ) -> Message:
        state = self.bot._get_state()
        channel = await channel._get_channel()

        if embed:
            embed = embed.to_dict()

        if allowed_mentions is not None:
            if state.allowed_mentions:
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
                    "Reference parameter must be either Message or MessageReference."
                ) from None

        if files:
            if file:
                files.append(file)

            if len(files) > 10:
                raise InvalidArgument("files parameter must be a list of up to 10 elements")
            elif not all(isinstance(file, File) for file in files):
                raise InvalidArgument("files parameter must be a list of File")

        elif file:
            files = [file]

        data = {
            "content": content,
            **self._get_components_json(components),
            **options,
            "embed": embed,
            "allowed_mentions": allowed_mentions,
            "tts": tts,
            "message_reference": reference,
        }

        if files:
            try:
                form = FormData()
                form.add_field(
                    "payload_json", dumps(data, separators=(",", ":"), ensure_ascii=True)
                )
                for index, file in enumerate(files):
                    form.add_field(
                        f"file{index}",
                        file.fp,
                        filename=file.filename,
                        content_type="application/octet-stream",
                    )

                data = await self.bot.http.request(
                    Route("POST", f"/channels/{channel.id}/messages"), data=form, files=files
                )

            finally:
                for f in files:
                    f.close()

        else:
            data = await self.bot.http.request(
                Route("POST", f"/channels/{channel.id}/messages"), json=data
            )

        msg = ComponentMessage(components=components, state=state, channel=channel, data=data)
        if delete_after is not None:
            self.bot.loop.create_task(msg.delete(delay=delete_after))
        return msg

    async def edit_component_msg(
        self,
        message: Message,
        content: str = None,
        *,
        embed: Embed = None,
        allowed_mentions: AllowedMentions = None,
        components: List[Union[Component, List[Component]]] = None,
        **options,
    ):
        state = self.bot._get_state()
        data = {**self._get_components_json(components), **options}

        if content is not None:
            data["content"] = content

        if embed:
            embed = embed.to_dict()
            data["embed"] = embed

        if allowed_mentions is not None:
            if state.allowed_mentions:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()

            data["allowed_mentions"] = allowed_mentions

        await self.bot.http.request(
            Route("PATCH", f"/channels/{message.channel.id}/messages/{message.id}"), json=data
        )

    def _get_components_json(
        self, components: List[Union[Component, List[Component]]] = None
    ) -> dict:
        if not isinstance(components, list) and not components:
            return {}

        for i in range(len(components)):
            if not isinstance(components[i], list):
                components[i] = [components[i]]

        lines = components
        return {
            "components": (
                [
                    {
                        "type": 1,
                        "components": [component.to_dict() for component in components],
                    }
                    for components in lines
                ]
                if lines
                else []
            ),
        }

    def _get_component_type(self, type: int):
        if type == 2:
            return Button
        elif type == 3:
            return Select

    def _structured_raw_data(self, raw_data: dict) -> dict:
        data = {
            "interaction": raw_data["d"]["id"],
            "interaction_token": raw_data["d"]["token"],
            "raw": raw_data,
        }
        raw_data = raw_data["d"]
        state = self.bot._get_state()

        components = []
        if "components" not in raw_data["message"]:
            components = []

            data["message"] = None
            data["user"] = None
        else:
            for line in raw_data["message"]["components"]:
                if line["type"] >= 2:
                    components.append(self._get_component_type(line["type"]).from_json(line))
                for component in line["components"]:
                    if component["type"] >= 2:
                        components.append(
                            self._get_component_type(component["type"]).from_json(component)
                        )

            data["message"] = ComponentMessage(
                state=state,
                channel=self.bot.get_channel(int(raw_data["channel_id"])),
                data=raw_data["message"],
                components=components,
            )

            if "member" in raw_data:
                userData = raw_data["member"]["user"]
            else:
                userData = raw_data["user"]
            data["user"] = User(state=state, data=userData)

        data["component"] = raw_data["data"]
        return data

    def _get_interaction(self, json: dict):
        data = self._structured_raw_data(json)
        rescomponent = []

        if data["message"]:
            for component in data["message"].components:
                if isinstance(component, Select):
                    for option in component.options:
                        if option.value in data["values"]:
                            if len(data["values"]) > 1:
                                rescomponent.append(option)
                            else:
                                rescomponent = [option]
                                break
                else:
                    if component.id == data["component"]["custom_id"]:
                        rescomponent = component
        else:
            rescomponent = data["component"]

        ctx = Interaction(
            bot=self.bot,
            client=self,
            user=data["user"],
            component=rescomponent,
            raw_data=data["raw"],
            message=data["message"],
            is_ephemeral=not bool(data["message"]),
        )
        return ctx

    async def fetch_component_message(self, message: Message) -> ComponentMessage:
        res = await self.bot.http.request(
            Route("GET", f"/channels/{message.channel.id}/messages/{message.id}")
        )
        components = []

        for i in res["components"]:
            components.append([])

            for j in i["components"]:
                components[-1].append(self._get_component_type(j["type"]).from_json(j))

        return ComponentMessage(
            channel=message.channel, state=self.bot._get_state(), data=res, components=components
        )
