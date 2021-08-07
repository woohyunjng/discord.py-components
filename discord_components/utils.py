from typing import List, Union, Optional
from .component import ActionRow, Component


__all__ = ("_get_components_json",)


def _get_components_json(
    components: List[Union[ActionRow, Component, List[Component]]] = None
) -> Optional[List[dict]]:
    if components is None:
        return None

    for i in range(len(components)):
        if isinstance(components[i], list):
            components[i] = ActionRow(*components[i])
        elif not isinstance(components[i], ActionRow):
            components[i] = ActionRow(components[i])

    lines = components
    return [row.to_dict() for row in lines] if lines else []
