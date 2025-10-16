from database.repositories import ObjectRepository

class ObjectService:
    def __init__(self, session):
        self.session = session
        self._object_repo = None

    @property
    def object_repo(self):
        if self._object_repo is None:
            self._object_repo = ObjectRepository(
                self.session
            )
        return self._object_repo

    async def get_all_objects(self):
        result = await self.object_repo.read()

        return list(result)

    async def get_objects_by(self, name):
        result = await self.object_repo.read(name = name)

        return result.first()