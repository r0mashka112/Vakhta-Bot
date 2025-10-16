from functools import wraps
from services import UserService

def require_registration(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        message = kwargs.get("message")
        session = kwargs.get("session")

        if message is None and args:
            message = args[0]

        if session is None:
            session = args[1] if len(args) > 1 else None

        if message is None or session is None:
            raise ValueError("Handler must receive 'message' and 'session'")

        user_service = UserService(session)

        user = await user_service.get_user_by(
            telegram_id = message.from_user.id
        )

        if not user:
            await message.answer("❌ Сначала зарегистрируйтесь через команду /start")
            return

        handler_kwargs = {k: kwargs[k] for k in kwargs if k in handler.__code__.co_varnames}
        handler_args = args[:len(handler.__code__.co_varnames)]

        return await handler(*handler_args, **handler_kwargs)

    return wrapper
