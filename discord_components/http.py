from typing import List

from discord import Client, File
from discord.http import Route

from .utils import _form_files


__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self, bot: Client):
        self.bot = bot

    def edit_response(
        self, interaction_token: str, data: dict, files: List[File] = None
    ):
        route = Route(
            "PATCH",
            f"/webhooks/{self.bot.user.id}/{interaction_token}/messages/@original",
        )

        if files is not None:
            return self.bot.http.request(
                route, data=_form_files(data, files), files=files
            )
        else:
            return self.bot.http.request(
                route,
                json=data,
            )

    def initial_response(
        self,
        interaction_id: int,
        interaction_token: str,
        data: dict,
        files: List[File] = None,
    ):
        route = Route(
            "POST",
            f"/interactions/{interaction_id}/{interaction_token}/callback",
        )

        if files is not None:
            return self.bot.http.request(
                route, data=_form_files(data, files), files=files
            )
        else:
            return self.bot.http.request(
                route,
                json=data,
            )
