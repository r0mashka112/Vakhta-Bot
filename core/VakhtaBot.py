from database import Database
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from core.middlewares import SessionMiddleware

class VakhtaBot:
    def __init__(self, token, db_url):
        self.bot = Bot(token = token)
        self.dp = Dispatcher()

        self.db = Database(url = db_url)

        self.dp.update.middleware(
            middleware = SessionMiddleware(self.db)
        )

    def include_routers(self, *routers):
        for router in routers:
            self.dp.include_router(router)

    async def launch(self):
        await self.bot.set_my_commands([
            BotCommand(command = "/start", description = "Запустить бота"),
            BotCommand(command = "/help", description = "Помощь"),
            BotCommand(command = "/export", description = "Экспортировать отчет")
        ])

        await self.bot.delete_webhook(
            drop_pending_updates = True
        )
        await self.dp.start_polling(self.bot)