from typing import Optional, List
from uuid import UUID

from sqlalchemy import select

from domain.persistence.repository import AbstractRepository, T
from domain.model.videoclip import Videoclip


class SQLAlchemyRepository(AbstractRepository[T]):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def get_one(self, id: UUID) -> Optional[T]:
        stmt = select(self._type_of_T).where(self._type_of_T == id)
        result = self.session.execute(stmt).one()
        return result

    def get_all(self) -> List[T]:
        results = self.session.query(self._type_of_T).all()
        return results

    def create(self, item: T):
        self.session.add(item)
        self.session.commit()


class VideoclipRepository(SQLAlchemyRepository[Videoclip]):
    def __init__(self, session):
        super().__init__(session)
