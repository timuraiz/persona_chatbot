from aiogram.fsm.state import StatesGroup, State


class SetPersona(StatesGroup):
    loading_persona = State()
    choosing_food_size = State()
