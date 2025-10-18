from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from core.config import (
    commands,
    commands_user_data
)

from utils import get_clean_text
from decorators import require_registration

from handlers.fsm import (
    Auth,
    ChangeUserData,
    ChooseObjectAndDate
)

from keyboards import (
    create_menu_keyboard,
    create_dynamic_keyboard,
    create_edit_profile_keyboard
)

from services import (
    UserService,
    ObjectService, SpecialityService
)

router = Router()

@router.message(StateFilter(None), F.text == 'Зарегистрироваться')
async def auth_handler(message: types.Message, state: FSMContext, session):
    user_service = UserService(session)

    user = await user_service.get_user_by(
        telegram_id = message.from_user.id
    )

    if user is None:
        await message.answer(
            text = 'Введите свое имя',
            reply_markup = ReplyKeyboardRemove()
        )
        await state.set_state(Auth.first_name)
    else:
        await message.answer(
            text = 'Вы уже зарегистрированы',
            reply_markup = create_menu_keyboard()
        )

@router.message(F.text.in_(commands))
@require_registration
async def action_handler(message: types.Message, state: FSMContext, session):
    async def _get_all_objects():
        return await ObjectService(session).get_all_objects()

    action = get_clean_text(message.text)

    if message.text == "ℹ️ Изменить мои данные":
        await message.answer(
            text = "Выберите пункт который хотите изменить",
            reply_markup = create_edit_profile_keyboard()
        )

    elif message.text == "📅 Планирую прибытие":
        objects = await _get_all_objects()

        await message.answer(
            text = "Выберите объект для планируемого прибытия:",
            reply_markup = create_dynamic_keyboard(
                objects = objects
            )
        )
        await state.update_data(action = action)
        await state.update_data(objects = objects)
        await state.set_state(ChooseObjectAndDate.object)
    elif message.text == "🛄 Планирую выезд":
        objects = await _get_all_objects()

        await message.answer(
            text = "Выберите объект для планируемого выезда:",
            reply_markup = create_dynamic_keyboard(
                objects = await _get_all_objects()
            )
        )
        await state.update_data(action = action)
        await state.update_data(objects = objects)
        await state.set_state(ChooseObjectAndDate.object)
    else:
        objects = await _get_all_objects()

        await message.answer(
            text = f"Выберите объект для действия '{action}':",
            reply_markup = create_dynamic_keyboard(
                objects = objects
            )
        )
        await state.update_data(action = action)
        await state.update_data(objects = objects)
        await state.set_state(ChooseObjectAndDate.object)


@router.message(
    F.text.in_(commands_user_data.values())
)
@require_registration
async def data_action_handler(message: types.Message, state: FSMContext, session):
    action = get_clean_text(message.text)

    if action == 'Фамилия':
        await message.answer(
            text = "Введите вашу фамилию",
            reply_markup = ReplyKeyboardRemove()
        )
        await state.set_state(ChangeUserData.last_name)
    elif action == 'Имя':
        await message.answer(
            text = "Введите ваше имя",
            reply_markup = ReplyKeyboardRemove()
        )
        await state.set_state(ChangeUserData.first_name)
    elif action == 'Отчество':
        await message.answer(
            text = "Введите ваше отчество",
            reply_markup = ReplyKeyboardRemove()
        )
        await state.set_state(ChangeUserData.middle_name)
    elif action == 'Специальность':
        speciality_service = SpecialityService(session)
        specialities = await speciality_service.get_all_specialities()

        await message.answer(
            text = "Выберите вашу специальность",
            reply_markup = create_dynamic_keyboard(
                objects = specialities
            )
        )

        await state.set_state(ChangeUserData.speciality)
    elif action == 'Телефон':
        await message.answer(
            text = (
                "Введите ваш номер телефона.\n"
                "Номер должен начинаться с +7"
            ),
            reply_markup = ReplyKeyboardRemove()
        )
        await state.set_state(ChangeUserData.phone)