from aiogram.types import Message

from services import UserService

def require_admin(handler):
    async def wrapper(message: Message, session):
        user_service = UserService(session)

        user = await user_service.get_user_by(
            telegram_id = message.from_user.id
        )

        if not user.is_admin:
            await message.answer(
                text = f"❌ Команда {message.text} доступна только администраторам"
            )
            return

        return await handler(message, session)

    return wrapper
