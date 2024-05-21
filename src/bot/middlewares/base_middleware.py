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
        logging.info(f'Checking access to the bot for chat_id={message.chat.id}')
        user: User = await User.get_by_username(message.from_user.username)
        if user:
            if user.chat_id is None:
                await User.update(user.id, chat_id=message.chat.id)
            logging.info('Handler was processed')
        else:
            await message.answer(BOT_REPLIES['general']['bot_is_not_allowed'])
            logging.info(f'Bot isn\'t allowed for this chat_id={message.chat.id}')
            return
        data['user_id'] = user.id
        await handler(message, data)
