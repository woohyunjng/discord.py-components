__all__ = ("Component",)


class Component:
    def to_dict(self) -> dict:
        raise NotImplementedError()

    def from_dict(self, data: dict):
        raise NotImplementedError()
