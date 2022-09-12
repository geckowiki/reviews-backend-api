from typing import AsyncGenerator
import uuid

from sqlalchemy import (
    Table,
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import func

from fastapi import Depends

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from fastapi_users_db_sqlalchemy.generics import GUID

from domain.model.user import User as UserDomain
from domain.model.videoclip import Videoclip as VideoclipDomain
from domain.model.review import Review as ReviewDomain
from app.settings import settings, DBDriver


Base = declarative_base()


convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

Base.metadata.naming_convention = convention


user_table = Table(
    "user",
    Base.metadata,
    Column("id", GUID, primary_key=True, default=uuid.uuid4),
    Column("email", String(length=320), unique=True, index=True, nullable=False),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("is_active", Boolean, default=False, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

videoclip_table = Table(
    "videoclip",
    Base.metadata,
    Column("id", GUID, primary_key=True, default=uuid.uuid4),
    Column("name", String(length=255), index=True, nullable=False),
    Column("filepath", String(length=255), nullable=False),
    Column("uploaded", DateTime(timezone=True), default=func.now()),
    Column("hash_id", String(length=64), index=True, unique=True, nullable=False),
    Column("author_id", ForeignKey("user.id")),
)

review_table = Table(
    "review",
    Base.metadata,
    Column("id", GUID, primary_key=True, default=uuid.uuid4),
    Column("imagepath", String(length=255), nullable=False),
    Column("text", Text, nullable=False),
    Column("hash_id", String(length=64), index=True, unique=True, nullable=False),
    Column("published", DateTime(timezone=True), default=func.now()),
    Column("videoclip_id", ForeignKey("videoclip.id")),
    Column("author_id", ForeignKey("user.id")),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __table__ = user_table

    def to_domain(self) -> UserDomain:
        return UserDomain(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
        )


async_engine = create_async_engine(settings.get_database_url(DBDriver.ASYNC))
async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

sync_engine = create_engine(settings.get_database_url(DBDriver.SYNC))
sync_session_maker = sessionmaker(bind=sync_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def map_to_domain():
    Base.registry.map_imperatively(UserDomain, user_table)
    review_mapper = Base.registry.map_imperatively(ReviewDomain, review_table)

    Base.registry.map_imperatively(
        VideoclipDomain,
        videoclip_table,
        properties={
            "reviews": relationship(
                review_mapper,
                collection_class=list,
            )
        },
    )
