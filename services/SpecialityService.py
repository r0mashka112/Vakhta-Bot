from database.repositories import SpecialityRepository

class SpecialityService:
    def __init__(self, session):
        self._speciality_repo = SpecialityRepository(
            session = session
        )

    async def get_all_specialities(self):
        return await self._speciality_repo.read(
            many = True
        )

    async def get_speciality_by(self, speciality_name: str):
        return await self._speciality_repo.read(
            name = speciality_name
        )