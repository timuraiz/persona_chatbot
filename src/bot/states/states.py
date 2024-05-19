from aiogram.fsm.state import StatesGroup, State


class SetPersona(StatesGroup):
    load_name = State()
    load_persona = State()


class ChatWithPersona(StatesGroup):
    in_chat = State()
