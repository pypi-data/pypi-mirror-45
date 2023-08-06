from typing import Any


class EdbackObject(object):
    def serialize(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: dict) -> Any:
        raise NotImplementedError()

