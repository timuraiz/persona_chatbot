from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from src.config.config import config

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    chat_id = Column(Integer, primary_key=True, unique=True)


class Persona(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.chat_id'), nullable=False)
    description = Column(Text, nullable=False)

    owner = relationship("User", back_populates="personas")


User.personas = relationship("Persona", back_populates="owner")


async def create_tables():
    from src.bot.db import DatabaseManager
    db_manager = DatabaseManager()
    await db_manager.connect()

    engine = create_engine(config.DATABASE_URL.replace("+asyncpg", ""), echo=True)
    Base.metadata.create_all(engine)


async def main():
    await create_tables()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
