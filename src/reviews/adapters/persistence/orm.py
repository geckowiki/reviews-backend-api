from typing import AsyncGenerator
import uuid

from sqlalchemy import Table, Column, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from fastapi import Depends

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from fastapi_users_db_sqlalchemy.generics import GUID

from domain.model.user import User as UserDomain
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


class User(SQLAlchemyBaseUserTableUUID, Base):
    __table__ = user_table


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
