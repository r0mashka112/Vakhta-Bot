from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

        if self.model is None:
            raise ValueError("The model is not listed in the repository")


    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj


    async def read(self, many = False, **filters):
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)

        if many:
            return result.scalars().all()

        return result.scalars().first()


    async def update(self, filters: dict, values: dict):
        stmt = (
            update(self.model)
            .filter_by(**filters)
            .values(**values)
            .returning(self.model)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.scalar_one_or_none()


    async def delete(self, filters: dict):
        stmt = delete(self.model).filter_by(**filters)

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.rowcount or 0