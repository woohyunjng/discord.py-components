from typing import Optional

from discord import Message

from .component import _get_component_type, ActionRow, Component

__all__ = ("ComponentMessage",)


class ComponentMessage(Message):
    __slots__ = tuple(list(Message.__slots__) + ["components"])

    def __init__(self, *, state, channel, data):
        super().__init__(state=state, channel=channel, data=data)

        components = []
        for i in data["components"]:
            components.append(ActionRow())
            for j in i["components"]:
                components[-1].append(_get_component_type(j["type"]).from_json(j))
        self.components = components

    def get_component(self, **checks) -> Optional[Component]:
        for row in self.components:
            for component in row["components"]:
                for key, value in checks:
                    if component.get(key) == value:
                        return component


def new_override(cls, *args, **kwargs):
    if isinstance(cls, Message):
        return object.__new__(ComponentMessage)
    else:
        return object.__new__(cls)


Message.__new__ = new_override
