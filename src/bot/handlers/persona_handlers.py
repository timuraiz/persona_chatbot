from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.states.states import SetPersona
from src.config.config import BOT_REPLIES

router = Router()


@router.message(Command("set_persona"))
async def set_persona(message: Message, state: FSMContext):
    await message.reply(BOT_REPLIES['commands']['set_persona'])
    await state.set_state(SetPersona.loading_persona)


@router.message(SetPersona.loading_persona)  # TODO: probably I need to validate message
async def food_chosen(message: Message, state: FSMContext):

    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
    await state.clear()


@router.message(Command("talk_with"))
async def talk_with(message: Message):
    await message.answer("Это текстовое сообщение!")


@router.message(Command("list_personas"))
async def list_personas(message: Message):
    await message.answer("Это стикер!")
