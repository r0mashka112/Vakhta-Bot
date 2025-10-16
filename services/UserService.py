from database.repositories import UserRepository
from database.repositories import SpecialityRepository

class UserService:
    def __init__(self, session):
        self.session = session
        self._user_repo = None
        self._speciality_repo = None

    @property
    def user_repo(self):
        if self._user_repo is None:
            self._user_repo = UserRepository(
                self.session
            )
        return self._user_repo


    @property
    def speciality_repo(self):
        if self._speciality_repo is None:
            self._speciality_repo = SpecialityRepository(
                self.session
            )
        return self._speciality_repo


    async def create_user(
            self,
            telegram_id: int,
            first_name: str,
            last_name: str,
            speciality_id: str,
            phone: str,
            middle_name: str = None
    ):
        new_user = await self.user_repo.create(
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
        telegram_id: int,
        first_name: str = None,
        last_name: str = None,
        speciality_name: str = None,
        phone: str = None,
        middle_name: str = None,
        is_admin: bool = None
    ):
        user_data = {
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "phone": phone,
            "is_admin": is_admin
        }

        if speciality_name is not None:
            speciality = await self.speciality_repo.read(
                name = speciality_name
            )

            user_data["speciality_id"] = speciality.id

        user = await self.user_repo.read(**user_data)

        return user.first()


    async def update_user(
            self,
            telegram_id: int,
            first_name: str = None,
            last_name: str = None,
            middle_name: str = None,
            speciality_name: str = None,
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

        if speciality_name is not None:
            result = await self.speciality_repo.read(
                name = speciality_name
            )

            speciality = result.first()

            if speciality:
                values["speciality_id"] = speciality.id

        if not values:
            return await self.get_user_by(
                telegram_id = telegram_id
            )

        updated_user = await self.user_repo.update(
            filters = {"telegram_id": telegram_id},
            values = values
        )

        return updated_user.first()


    async def get_admins(self):
        admin_data = {
            "is_admin": True
        }

        admins = await self.user_repo.read(**admin_data)

        return admins.all()