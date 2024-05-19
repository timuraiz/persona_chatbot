import asyncio
import logging
from aiogram import Bot, Dispatcher

from src.config.config import config
from src.bot.handlers import (
    base_router,
    persona_router
)
from src.bot.middlewares import CheckAccessMiddleware
from src.bot.tables import async_db_session

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    await async_db_session.init()

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


if __name__ == "__main__":
    asyncio.run(main())
