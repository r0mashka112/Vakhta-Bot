from aiogram import Router, types
from aiogram.filters.command import Command

from keyboards import create_auth_keyboard,\
    create_menu_keyboard

from utils import get_full_name

from decorators import require_registration,\
    require_admin

from services import (
    UserService,
    ReportService
)

router = Router()

@router.message(Command('start'))
async def start_handler(message: types.Message, session) -> None:
    user_service = UserService(session)

    user = await user_service.get_user_by(
        telegram_id = message.from_user.id
    )

    if user is None:
        await message.answer(
            text = 'Добро пожаловать!\n\nДля начала нужно пройти регистрацию.',
            reply_markup = create_auth_keyboard()
        )
    else:
        await message.answer(
            text = f'Привет, <strong>{get_full_name(user)}</strong>!\n\nВы зарегистрированы.',
            parse_mode = 'HTML'
        )

        await message.answer(
            text = 'Выберите действие:',
            reply_markup = create_menu_keyboard()
        )


@router.message(Command('help'))
async def help_handler(message: types.Message) -> None:
    await message.answer(
        text = "Доступные действия:\n"
             "✅ Прибыл — отметить прибытие\n"
             "❌ Убыл — отметить убытие\n"
             "📅 Планирую прибытие — указать дату/время\n"
             "🛄 Планирую выезд — указать дату/время\n"
             "🤒 Заболел — сообщить о болезни\n"
             "⏱️ Задерживаюсь — сообщить о задержке\n"
    )

@router.message(Command('export'))
@require_registration
@require_admin
async def export_handler(message: types.Message, session) -> None:
    report_service = ReportService(session)

    excel_buffer = await report_service.generate_report()

    await message.answer_document(
        document = types.BufferedInputFile(
            excel_buffer.getvalue(),
            filename = "Посещаемость.xlsx"
        ),
        caption = "Отчёт по посещаемости"
    )