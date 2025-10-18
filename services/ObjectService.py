from database.repositories import ObjectRepository

class ObjectService:
    def __init__(self, session):
        self._object_repo = ObjectRepository(
            session
        )

    async def get_all_objects(self):
        return await self._object_repo.read(many = True)


    async def get_object_by(self, name):
        return await self._object_repo.read(name = name)