from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Новый день"),
            KeyboardButton(text="ЗП")
        ]
    ]
)



