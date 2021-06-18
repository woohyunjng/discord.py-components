from discord import Message

from .component import _get_component_type, ActionRow

__all__ = ("ComponentMessage",)


class ComponentMessage(Message):
    def __init__(self, *, data: dict, **kwargs):
        super().__init__(**kwargs, data=data)

        components = []
        for i in data["components"]:
            if i["type"] == 1:
                components.append(ActionRow())
                for j in i["components"]:
                    components[-1].append(_get_component_type(j["type"]).from_json(j))
            else:
                components.append(_get_component_type(i["type"]).from_json(i))
        self.components = components
