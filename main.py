import asyncio
import logging

from core import VakhtaBot
from core.config import settings

from handlers import (
    command_router,
    message_router
)

from handlers.fsm import (
    fsm_auth_router,
    fsm_edit_my_data_router,
    fsm_choose_object_and_date_router
)

async def main() -> None:
    bot = VakhtaBot(
        token = settings.BOT_TOKEN,
        db_url = settings.DATABASE_URL_AIOSQLITE
    )

    bot.include_routers(
        command_router,
        message_router,
        fsm_auth_router,
        fsm_edit_my_data_router,
        fsm_choose_object_and_date_router
    )

    await bot.launch()

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())