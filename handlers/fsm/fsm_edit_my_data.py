import re

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import (
    create_menu_keyboard,
    create_dynamic_keyboard
)

from services import (
    UserService,
    SpecialityService
)

router = Router()

class ChangeUserData(StatesGroup):
    first_name = State()
    last_name = State()
    middle_name = State()
    speciality = State()
    phone = State()

@router.message(ChangeUserData.first_name)
async def first_name_received(message: types.Message, state: FSMContext, session):
    user_service = UserService(session)

    updated_user = await user_service.update_user(
        telegram_id = message.from_user.id,
        first_name = message.text
    )

    await message.answer(
        text = f'Вы изменили свое имя на "{updated_user.first_name}"',
        reply_markup = create_menu_keyboard()
    )

    await state.clear()


@router.message(ChangeUserData.last_name)
async def last_name_received(message: types.Message, state: FSMContext, session):
    user_service = UserService(session)

    updated_user = await user_service.update_user(
        telegram_id = message.from_user.id,
        last_name = message.text
    )

    await message.answer(
        text = f'Вы изменили свою фамилию на "{updated_user.last_name}"',
        reply_markup = create_menu_keyboard()
    )

    await state.clear()


@router.message(ChangeUserData.middle_name)
async def middle_name_received(message: types.Message, state: FSMContext, session):
    user_service = UserService(session)

    updated_user = await user_service.update_user(
        telegram_id = message.from_user.id,
        middle_name = message.text
    )

    await message.answer(
        text = f'Вы изменили свое отчество на "{updated_user.middle_name}"',
        reply_markup = create_menu_keyboard()
    )

    await state.clear()


@router.message(ChangeUserData.speciality)
async def speciality_received(message: types.Message, state: FSMContext, session):
    user_service = UserService(session)
    speciality_service = SpecialityService(session)

    speciality = await speciality_service.get_speciality_by(
        speciality_name = message.text
    )

    if speciality is None:
        all_specialities = await speciality_service\
            .get_all_specialities()

        await message.answer(
            text = 'Выберите вашу специальность из списка',
            reply_markup = create_dynamic_keyboard(
                objects = all_specialities
            )
        )
        return

    updated_user = await user_service.update_user(
        telegram_id = message.from_user.id,
        speciality_name = speciality.name
    )

    await message.answer(
        text = f'Вы изменили свою специальность на "{speciality.name}"',
        reply_markup = create_menu_keyboard()
    )

    await state.clear()


@router.message(ChangeUserData.phone)
async def phone_received(message: types.Message, state: FSMContext, session):
    cleaned_phone = re.sub(r'[\s\(\)\-]', '', message.text)
    phone_is_correct = False

    if re.match(r'^\+7\d{10}$', cleaned_phone):
        phone_is_correct = True

    if re.match(r'^8\d{10}$', cleaned_phone):
        cleaned_phone = '+7' + cleaned_phone[1:]
        phone_is_correct = True

    if not phone_is_correct:
        await message.answer(
            text = (
                'Введен некорректный номер телефона.\n'
                'Номер должен начинаться с +7'
            )
        )
        return

    user_service = UserService(session)

    updated_user = await user_service.update_user(
        telegram_id = message.from_user.id,
        phone = cleaned_phone
    )

    await message.answer(
        text = f'Вы изменили свой номер телефона на "{updated_user.phone}"',
        reply_markup = create_menu_keyboard()
    )

    await state.clear()