from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

from src.bot.tables import User
from src.config.config import BOT_REPLIES


class CheckAccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:
        logging.info(f"Checking access to the bot for chat_id={message.chat.id}")
        exists = await User.get(message.chat.id)
        if exists:
            await handler(message, data)
            logging.info("Handler was processed")
        else:
            await message.answer(BOT_REPLIES['general']['bot_is_not_allowed'])
            logging.info(f"Bot isn't allowed for this chat_id={message.chat.id}")
