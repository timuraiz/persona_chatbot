from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.states import SetPersona, ChatWithPersona
from src.bot.tables import Persona, User
from src.config.config import BOT_REPLIES
from src.bot.utils.keyboard import get_bye_button
from src.bot.utils.gpt import GptAPI

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
async def load_persona(message: Message, state: FSMContext, user_id: int):
    data = await state.get_data()
    name = data['name']
    persona = message.text
    await Persona.create(owner_id=user_id, name=name, description=persona)

    await message.reply(text=BOT_REPLIES['commands']['set_persona']['saved'])
    await state.clear()


@router.message(Command("list_personas"))
async def list_personas(message: Message, user_id: int):
    rows = await Persona.all(user_id)
    if not rows:
        await message.answer(BOT_REPLIES['commands']['list_personas']['no_personas'])
    else:
        header = BOT_REPLIES['commands']['list_personas']['header']
        personas_list = '\n'.join([f'- {persona[0].name} 👤' for persona in rows])
        footer = BOT_REPLIES['commands']['list_personas']['footer']
        await message.answer(f"{header}\n{personas_list}\n\n{footer}")


@router.message(Command("talk_with"))
async def talk_with(message: Message, state: FSMContext, user_id: int):
    msg_text = message.text.strip().split(maxsplit=1)
    if len(msg_text) != 2:
        await message.answer(BOT_REPLIES['commands']['talk_with']['not_provided_name'])
        return
    persona_name = message.text.strip().split(maxsplit=1)[1]
    persona: Persona = await Persona.get_by_name(owner_id=user_id, name=persona_name)
    if persona:
        await state.update_data(name=persona_name, persona=persona.description, conversation=[])
        await state.set_state(ChatWithPersona.in_chat)
    await message.answer(
        BOT_REPLIES['commands']['talk_with']['found'] if persona else BOT_REPLIES['commands']['talk_with']['not_found'],
        reply_markup=get_bye_button()
    )


@router.message(ChatWithPersona.in_chat, F.text.lower() != 'bye')
async def talking(message: Message, state: FSMContext):
    user_data = await state.get_data()
    api = GptAPI()
    user_data['conversation'].append(message.text)
    generated_text = await api.ask(
        name=user_data['name'], persona=user_data['persona'], messages=user_data['conversation']
    )
    user_data['conversation'].append(generated_text)

    await state.update_data(conversation=user_data['conversation'])
    await message.answer(generated_text, reply_markup=get_bye_button())


@router.message(ChatWithPersona.in_chat, F.text.lower() == 'bye')
async def quit_talking(message: Message, state: FSMContext):
    await message.answer(BOT_REPLIES['commands']['talk_with']['bye'], reply_markup=ReplyKeyboardRemove())
    await state.clear()
