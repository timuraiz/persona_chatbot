import sqlalchemy as sa
from databases import Database
import logging
from functools import wraps

from src.config.config import config
from src.bot.tables import User, Persona


class DatabaseManager:
    def __init__(self):
        self.database = Database(config.DATABASE_URL)

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()

    @staticmethod
    def db_method(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            await self.connect()
            try:
                result = await func(self, *args, **kwargs)
                logging.info(f"RESULT: {result}")
                return result
            finally:
                await self.disconnect()

        return wrapper

    @db_method
    async def add_user(self, chat_id: int):
        exists = await self.user_exists(chat_id)
        if exists:
            return
        logging.info(f"User does not exist with chat_id: {chat_id}")
        return await self._execute_query(sa.insert(User).values(chat_id=chat_id))

    @db_method
    async def user_exists(self, chat_id: int) -> bool:
        result = await self._execute_query(sa.select(User).where(User.chat_id == chat_id))
        exists = result is not None
        logging.info(f"User {'exists' if exists else 'does not exist'} with chat_id: {chat_id}")
        return exists

    @db_method
    async def _execute_query(self, query):
        return await self.database.execute(query)
