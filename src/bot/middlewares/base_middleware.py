from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

from src.bot.db import DatabaseManager
from src.config.config import BOT_REPLIES

db_manager = DatabaseManager()


class CheckAccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:
        logging.info(f"Checking access to the bot for chat_id={message.chat.id}")
        exists = await db_manager.user_exists(message.chat.id)
        if exists:
            await handler(message, data)
            logging.info("Handler was processed")
        else:
            await message.answer(BOT_REPLIES['general']['bot_is_not_allowed'])
            logging.info(f"Bot isn't allowed for this chat_id={message.chat.id}")
