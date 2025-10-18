from database.repositories import UserRepository

class UserService:
    def __init__(self, session):
        self._user_repo = UserRepository(
            session
        )

    async def create_user(
            self,
            telegram_id: int,
            first_name: str,
            last_name: str,
            speciality_id: str,
            phone: str,
            middle_name: str = None
    ):
        new_user = await self._user_repo.create(
            telegram_id = telegram_id,
            first_name = first_name,
            last_name = last_name,
            middle_name = middle_name,
            speciality_id = speciality_id,
            phone = phone
        )

        return new_user


    async def get_user_by(
        self,
        telegram_id: int
    ):
        user_data = {
            "telegram_id": telegram_id
        }

        return await self._user_repo.read(**user_data)


    async def update_user(
            self,
            telegram_id: int,
            first_name: str = None,
            last_name: str = None,
            middle_name: str = None,
            speciality_id: str = None,
            phone: str = None
    ):
        values = {}

        if first_name is not None:
            values["first_name"] = first_name
        if last_name is not None:
            values["last_name"] = last_name
        if middle_name is not None:
            values["middle_name"] = middle_name
        if phone is not None:
            values["phone"] = phone
        if speciality_id is not None:
            values["speciality_id"] = speciality_id

        return await self._user_repo.update(
            filters = {"telegram_id": telegram_id},
            values = values
        )


    async def get_admins(self):
        admin_data = {
            "is_admin": True
        }

        return await self._user_repo.read(many = True, **admin_data)