from typing import TypeVar, Generic


T_id = TypeVar("T_id")


class Entity(Generic[T_id]):
    id: T_id

    def __init__(self, id: T_id) -> None:
        self.id = id

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)
