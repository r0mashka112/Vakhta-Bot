from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_send_phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📱 Отправить номер", request_contact = True)]
        ],
        resize_keyboard = True,
        one_time_keyboard = True
    )