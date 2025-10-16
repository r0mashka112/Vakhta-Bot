from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_auth_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = 'Зарегистрироваться')]
        ],
        resize_keyboard = True
    )