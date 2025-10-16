from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
ENV_FILE_PATH = PROJECT_ROOT / '.env'

commands = [
    "✅ Прибыл",
    "❌ Убыл",
    "📅 Планирую прибытие",
    "🛄 Планирую выезд",
    "🤒 Заболел",
    "⏱️ Задерживаюсь",
    "ℹ️ Изменить мои данные"
]

commands_user_data = {
    "last_name": "👤 Фамилия",
    "first_name": "👤 Имя",
    "middle_name": "👤 Отчество",
    "speciality": "🎓 Специальность",
    "phone": "📞 Телефон"
}

class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_PATH: str

    @property
    def DATABASE_URL_AIOSQLITE(self):
        absolute_db_path = PROJECT_ROOT / self.DB_PATH
        return f'sqlite+aiosqlite:///{absolute_db_path}'

    model_config = SettingsConfigDict(
        env_file = ENV_FILE_PATH,
        env_file_encoding = 'utf-8'
    )

settings = Settings()
