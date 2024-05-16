import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from src.config.config import config

logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.BOT_TOKEN.get_secret_value())
# Диспетчер
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
