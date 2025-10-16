from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text = '✅ Прибыл'),
                KeyboardButton(text = '❌ Убыл')
             ],
            [
                KeyboardButton(text = '📅 Планирую прибытие'),
                KeyboardButton(text = '🛄 Планирую выезд')
            ],
            [
                KeyboardButton(text = '🤒 Заболел'),
                KeyboardButton(text = '⏱️ Задерживаюсь')
            ],
            [
                KeyboardButton(text = 'ℹ️ Изменить мои данные')
            ]
        ],
        resize_keyboard = True,
        one_time_keyboard = True
    )