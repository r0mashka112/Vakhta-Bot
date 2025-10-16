from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_yes_or_no_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = 'Да')],
            [KeyboardButton(text = 'Нет')]
        ],
        resize_keyboard = True,
        one_time_keyboard = True
    )