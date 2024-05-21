import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config.config import config

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        self._engine = create_async_engine(config.DATABASE_URL, echo=True)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


async_db_session = AsyncDatabaseSession()


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sa.update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = sa.select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result


# class User(Base, ModelAdmin):
#     __tablename__ = 'users'
#
#     chat_id = Column(Integer, primary_key=True, unique=True)
#     personas = relationship('Persona', back_populates='owner')
#     __mapper_args__ = {'eager_defaults': True}
#
#     @classmethod
#     async def get(cls, id: int):
#         query = sa.select(cls).where(cls.chat_id == id)
#         results = await async_db_session.execute(query)
#         result = results.one_or_none()
#         if result is not None:
#             result, = result
#         return result
#
#
# class Persona(Base, ModelAdmin):
#     __tablename__ = 'personas'
#
#     id = Column(Integer, primary_key=True)
#     owner_id = Column(Integer, ForeignKey('users.chat_id'), nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(Text, nullable=False)
#     owner = relationship('User')
#
#     @classmethod
#     async def all(cls, owner_id: int):
#         query = sa.select(cls).where(cls.owner_id == owner_id)
#         results = await async_db_session.execute(query)
#         return results.all()
#
#     @classmethod
#     async def get_by_name(cls, owner_id: int, name: str):
#         query = sa.select(cls).where(sa.and_(cls.name == name, cls.owner_id == owner_id))
#         results = await async_db_session.execute(query)
#         result = results.one_or_none()
#         if result is not None:
#             result, = result
#         return result


class User(Base, ModelAdmin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    chat_id = Column(Integer, unique=True, nullable=True)

    personas = relationship('Persona', back_populates='owner', cascade="all, delete-orphan")

    @classmethod
    async def get_by_username(cls, username):
        query = sa.select(cls).where(cls.username == username)
        results = await async_db_session.execute(query)
        result = results.one_or_none()
        if result is not None:
            result, = result
        return result


class Persona(Base, ModelAdmin):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    owner = relationship('User', back_populates='personas')

    @classmethod
    async def all(cls, owner_id: int):
        query = sa.select(cls).where(cls.owner_id == owner_id)
        results = await async_db_session.execute(query)
        return results.all()

    @classmethod
    async def get_by_name(cls, owner_id: int, name: str):
        query = sa.select(cls).where(cls.name == name, cls.owner_id == owner_id)
        results = await async_db_session.execute(query)
        result = results.scalar_one_or_none()
        return result


async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()


if __name__ == '__main__':
    import asyncio

    asyncio.run(init_app())
