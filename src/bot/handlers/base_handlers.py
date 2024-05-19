from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from src.config.config import BOT_REPLIES
from src.bot.tables import User

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(BOT_REPLIES['commands']['start'])
    await User.create(chat_id=message.chat.id)

# @router.message(F.text.lower() == "да")
# async def answer_yes(message: Message):
#     await message.answer(
#         "Это здорово!",
#         reply_markup=ReplyKeyboardRemove()
#     )
#
#
# @router.message(F.text.lower() == "нет")
# async def answer_no(message: Message):
#     await message.answer(
#         "Жаль...",
#         reply_markup=ReplyKeyboardRemove()
#     )
