from discord import Message
from typing import List, Union

from .component import Component


class ComponentMessage(Message):
    def __init__(self, *, components: List[Union[Component, List[Component]]] = [], **kwargs):
        super().__init__(**kwargs)
        self.components = components
