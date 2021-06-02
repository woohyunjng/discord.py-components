from discord import Message
from typing import List, Union

from .component import Component


class ComponentMessage(Message):
    def __init__(
        self, *, components: Union[List[Component], List[List[Component]]] = None, **kwargs
    ):
        super().__init__(**kwargs)
        if components is None:
            components = []
        self.components = components
