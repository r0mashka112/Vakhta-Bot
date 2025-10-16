from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_dynamic_keyboard(objects: list, row_width: int = 2) -> ReplyKeyboardMarkup:
    rows, row = [], []

    for i, obj in enumerate(objects, start = 1):
        row.append(KeyboardButton(text = obj.name))

        if i % row_width == 0:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    return ReplyKeyboardMarkup(
        keyboard = rows,
        resize_keyboard = True
    )
