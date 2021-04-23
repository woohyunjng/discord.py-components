from typing import Union, Optional
from uuid import uuid1


class Button:
    def __init__(
        self,
        *,
        style: Union["blue", "gray", "green", "red", "url", int],
        label: str,
        id: Optional[str] = None,
        url: Optional[str] = None
    ):
        self.style = (
            {"blue": 1, "gray": 2, "green": 3, "red": 4, "url": 5}[style]
            if isinstance(style, str)
            else style
        )
        self.label = label
        if url:
            self.id = None
        else:
            self.id = id or str(uuid1())
        self.url = url
