from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_bye_button() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Bye")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, input_field_placeholder='Type some message to selected persona')
