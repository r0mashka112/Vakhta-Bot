from database.repositories import SpecialityRepository

class SpecialityService:
    def __init__(self, session):
        self.session = session
        self._speciality_repo = None

    @property
    def speciality_repo(self):
        if self._speciality_repo is None:
            self._speciality_repo = SpecialityRepository(
                self.session
            )
        return self._speciality_repo


    async def get_all_specialities(self):
        result = await self.speciality_repo.read()

        return list(result)

    async def get_speciality_by(self, speciality_name: str):
        speciality = await self.speciality_repo.read(
            name = speciality_name
        )

        return speciality.first()