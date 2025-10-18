from datetime import datetime

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup

from keyboards import create_menu_keyboard

from services import (
    UserService,
    AttendanceService
)

router = Router()

class ChooseObjectAndDate(StatesGroup):
    object = State()
    planned_date = State()

@router.message(
    ChooseObjectAndDate.object,
    F.text
)
async def object_name_received(message: types.Message, state: FSMContext, session):
    data = await state.get_data()

    action = data.get('action')
    objects = data.get('objects')

    chosen_object = next(
        filter(lambda obj: obj.name == message.text, objects),
        None
    )

    if chosen_object is None:
        await message.answer(
            text = "❌ Пожалуйста, выберите объект из списка:"
        )
        return

    user_service = UserService(session)
    attendance_service = AttendanceService(session)

    user = await user_service.get_user_by(
        telegram_id = message.from_user.id
    )

    attendance_data = {
        'user_id': user.id,
        'object_id': chosen_object.id,
        'action': action
    }

    attendance = await attendance_service \
        .get_attendance_by(**attendance_data)

    if attendance is not None:
        await message.answer(
            text = f'Вы уже выбрали объект {chosen_object.name}',
            reply_markup = create_menu_keyboard()
        )
        await state.clear()
        return

    await state.update_data(user_id = user.id)
    await state.update_data(object_id = chosen_object.id)
    await state.update_data(object_name = chosen_object.name)

    if action is None:
        raise ValueError("A variable 'action' cannot be None")
    else:
        match action:
            case 'Планирую прибытие':
                await message.answer(
                    text = 'Введите планируемую дату прибытия в формате ДД.ММ.ГГГГ',
                    reply_markup = ReplyKeyboardRemove()
                )
                await state.set_state(
                    ChooseObjectAndDate.planned_date
                )
            case 'Планирую выезд':
                await message.answer(
                    text = 'Введите планируемую дату отъезда в формате ДД.ММ.ГГГГ',
                    reply_markup = ReplyKeyboardRemove()
                )
                await state.set_state(
                    ChooseObjectAndDate.planned_date
                )
            case 'Прибыл' | 'Убыл' | 'Заболел' | 'Задерживаюсь':
                await attendance_service.create_attendance(
                    user_id = user.id,
                    object_id = chosen_object.id,
                    date = datetime.now().strftime("%d.%m.%Y"),
                    action = action
                )

                await message.answer(
                    text = f"Вы выбрали объект {chosen_object.name}",
                    reply_markup = create_menu_keyboard()
                )
                await state.clear()
            case _:
                raise ValueError(f"Unrecognized action: {action}")

@router.message(
    ChooseObjectAndDate.planned_date,
    F.text
)
async def planned_date_received(message: types.Message, state: FSMContext, session):
    planned_date = datetime.strptime(message.text, "%d.%m.%Y").date()

    if planned_date < datetime.now().date():
        await message.answer("Дата не может быть в прошлом. Введите корректную дату:")
        return

    data = await state.get_data()

    attendance_data = {
        'user_id': data.get('user_id'),
        'object_id': data.get('object_id'),
        'date': planned_date.strftime("%d.%m.%Y"),
        'action': data.get('action')
    }

    attendance_service = AttendanceService(session)

    new_attendance = await attendance_service\
        .create_attendance(**attendance_data)

    if data.get('action') == 'Планирую прибытие':
        await message.answer(
            text = f"Вы запланировали прибытие на объект {data.get('object_name')}.\n\n"
                  f"Планируемая дата прибытия: {new_attendance.date}",
            reply_markup = create_menu_keyboard()
        )
    elif data.get('action') == 'Планирую выезд':
        await message.answer(
            text = f"Вы запланировали выезд с объекта {data.get('object_name')}.\n\n"
                  f"Планируемая дата выезда: {new_attendance.date}",
            reply_markup = create_menu_keyboard()
        )

    await state.clear()