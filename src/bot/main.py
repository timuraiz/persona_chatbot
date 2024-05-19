import asyncio
import logging
from aiogram import Bot, Dispatcher

from src.config.config import config
from src.bot.handlers import (
    base_router,
    persona_router
)
from src.bot.db import DatabaseManager
from src.bot.middlewares import CheckAccessMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN.get_secret_value())

dp = Dispatcher()


async def main():
    db_manager = DatabaseManager()
    await db_manager.connect()
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        base_router,
        persona_router
    )

    # Setup custom logging middleware
    base_router.message.middleware(CheckAccessMiddleware())
    persona_router.message.middleware(CheckAccessMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
        await db_manager.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
