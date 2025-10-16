from core.config import commands_user_data
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_edit_profile_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(
                    text = commands_user_data.get('last_name')
                ),
                KeyboardButton(
                    text = commands_user_data.get('first_name')
                ),
                KeyboardButton(
                    text = commands_user_data.get('middle_name')
                )
            ],
            [
                KeyboardButton(
                    text = commands_user_data.get('speciality')
                ),
                KeyboardButton(
                    text = commands_user_data.get('phone')
                )
            ]
        ],
        resize_keyboard = True
    )