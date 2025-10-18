from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import get_full_name

from keyboards import (
    create_menu_keyboard,
    create_dynamic_keyboard,
    create_yes_or_no_keyboard,
    create_send_phone_keyboard
)

from services import (
    UserService,
    SpecialityService
)

router = Router()

class Auth(StatesGroup):
    first_name = State()
    last_name = State()
    has_middle_name = State()
    middle_name = State()
    speciality = State()
    phone = State()

@router.message(Auth.first_name)
async def first_name_received(message: types.Message, state: FSMContext):
    await state.update_data(first_name = message.text)
    await message.answer(
        text = 'Теперь укажите свою фамилию'
    )
    await state.set_state(Auth.last_name)


@router.message(Auth.last_name)
async def last_name_received(message: types.Message, state: FSMContext):
    await state.update_data(last_name = message.text)
    await message.answer(
        text = 'У вас есть отчество',
        reply_markup = create_yes_or_no_keyboard()
    )
    await state.set_state(Auth.has_middle_name)

@router.message(
    Auth.has_middle_name,
    F.text.lower().in_(['да', 'нет'])
)
async def has_middle_name_received(message: types.Message, state: FSMContext, session):
    if message.text.lower() == 'да':
        await message.answer(
            text = 'Укажите ваше отчество'
        )
        await state.set_state(Auth.middle_name)
    else:
        speciality_service = SpecialityService(session)

        all_specialities = await speciality_service\
            .get_all_specialities()

        await message.answer(
            text = 'Выберите вашу специальность',
            reply_markup = create_dynamic_keyboard(
                objects = all_specialities
            )
        )
        await state.set_state(Auth.speciality)


@router.message(Auth.middle_name)
async def middle_name_received(message: types.Message, state: FSMContext, session):
    await state.update_data(middle_name = message.text)

    speciality_service = SpecialityService(session)

    all_specialities = await speciality_service\
        .get_all_specialities()

    await message.answer(
        text = 'Выберите вашу специальность',
        reply_markup = create_dynamic_keyboard(
            objects = all_specialities
        )
    )

    await state.set_state(Auth.speciality)

@router.message(Auth.speciality)
async def speciality_received(message: types.Message, state: FSMContext, session):
    speciality_service = SpecialityService(session)

    speciality = await speciality_service\
        .get_speciality_by(speciality_name = message.text)

    if speciality is None:
        await message.answer(
            text = 'Выберите вашу специальность из списка'
        )
        return

    await state.update_data(speciality_id = speciality.id)

    await message.answer(
        text = 'Поделитесь вашим номером телефона',
        reply_markup = create_send_phone_keyboard()
    )

    await state.set_state(Auth.phone)

@router.message(Auth.phone)
async def phone_received(message: types.Message, state: FSMContext, session):
    await state.update_data(phone = f'+{message.contact.phone_number}')

    user_data = await state.get_data()
    user_data['telegram_id'] = message.from_user.id

    user_service = UserService(session)

    new_user = await user_service.create_user(
        telegram_id = user_data.get('telegram_id'),
        first_name = user_data.get('first_name'),
        last_name = user_data.get('last_name'),
        middle_name = user_data.get('middle_name', None),
        speciality_id = user_data.get('speciality_id'),
        phone = user_data.get('phone')
    )

    admins = await user_service.get_admins()

    for admin in admins:
        await message.bot.send_message(
            chat_id = admin.telegram_id,
            text = (
                f"👤 Новый пользователь!\n"
                f"ФИО: {get_full_name(new_user)}\n"
                f"Telegram ID: {new_user.telegram_id}\n"
            )
        )

    await message.answer(
        text = (
            f'✅ Регистрация завершена.\n\n'
            f'Привет, <strong>{get_full_name(new_user)}</strong>'
        ),
        parse_mode = 'HTML'
    )

    await message.answer(
        text = 'Теперь вы можете отмечаться и планировать перемещения.\n\n'
           'С полным списком действий вы можете ознакомить с помощью команды /help',
        reply_markup = create_menu_keyboard()
    )

    await state.clear()
