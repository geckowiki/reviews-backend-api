from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from domain.persistence.repository import AbstractRepository, T
from domain.model.videoclip import Videoclip
from domain.model.review import Review


class SQLAlchemyRepository(AbstractRepository[T]):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def get_one(self, id_: UUID) -> Optional[T]:
        stmt = select(self._type_of_T).where(self._type_of_T.id == id_)
        try:
            result = self.session.execute(stmt).one()[0]
        except NoResultFound:
            return None
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


class ReviewRepository(SQLAlchemyRepository[Review]):
    def __init__(self, session):
        super().__init__(session)
