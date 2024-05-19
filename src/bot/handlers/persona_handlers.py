from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.states import SetPersona, ChatWithPersona
from src.bot.tables import Persona
from src.config.config import BOT_REPLIES
from src.bot.utils.keyboard import get_bye_button

router = Router()


@router.message(Command("set_persona"))
async def set_persona(message: Message, state: FSMContext):
    await message.reply(BOT_REPLIES['commands']['set_persona']['load_name'])
    await state.set_state(SetPersona.load_name)


@router.message(SetPersona.load_name)
async def load_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply(BOT_REPLIES['commands']['set_persona']['load_persona'])
    await state.set_state(SetPersona.load_persona)


@router.message(SetPersona.load_persona)
async def load_persona(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    persona = message.text
    await Persona.create(owner_id=message.chat.id, name=name, description=persona)

    await message.reply(text=BOT_REPLIES['commands']['set_persona']['saved'])
    await state.clear()


@router.message(Command("list_personas"))
async def list_personas(message: Message):
    rows = await Persona.all(message.chat.id)
    await message.answer('\n'.join([f'- {persona[0].name}' for persona in rows]))


@router.message(Command("talk_with"))
async def talk_with(message: Message, state: FSMContext):
    persona_name = message.text.strip().split()[1]
    persona: Persona = await Persona.get_by_name(persona_name)
    if persona:
        await state.update_data(name=persona.description)
        await state.set_state(ChatWithPersona.in_chat)
    await message.answer(
        BOT_REPLIES['commands']['talk_with']['found'] if persona else BOT_REPLIES['commands']['talk_with']['not_found'],
        reply_markup=get_bye_button()
    )


@router.message(ChatWithPersona.in_chat, F.text.lower() != 'bye')
async def talking(message: Message, state: FSMContext):
    generated_text = 'generated text'
    await message.answer(generated_text, reply_markup=get_bye_button())


@router.message(ChatWithPersona.in_chat, F.text.lower() == 'bye')
async def quit_talking(message: Message, state: FSMContext):
    await message.answer(BOT_REPLIES['commands']['talk_with']['bye'], reply_markup=ReplyKeyboardRemove())
    await state.clear()
