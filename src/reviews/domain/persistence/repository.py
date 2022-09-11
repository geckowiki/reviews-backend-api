from uuid import UUID
from typing import TypeVar, Generic, Optional, get_args, Any, List
import abc


T = TypeVar("T")


class AbstractRepository(Generic[T]):
    _type_of_T: Any

    def __init_subclass__(cls) -> None:
        cls._type_of_T = get_args(cls.__orig_bases__[0])[0]
    
    @abc.abstractmethod
    def get_one(self, id: UUID) -> Optional[T]:
        ...
    
    @abc.abstractmethod
    def get_all(self) -> List[T]:
        ...
    
    @abc.abstractmethod
    def create(self, item: T):
        ...