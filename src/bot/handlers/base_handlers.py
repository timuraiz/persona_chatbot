from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from src.config.config import BOT_REPLIES
from src.bot.tables import User

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(BOT_REPLIES['commands']['start'])


@router.message(Command('help'))
async def help(message: Message):
    await message.answer(BOT_REPLIES['commands']['help'])
