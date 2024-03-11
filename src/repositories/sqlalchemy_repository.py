from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.abstract_repository import AbstractRepository
from src.utils.validators import no_result_found_handler


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @no_result_found_handler()
    async def get_one(self, id: int):
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_one(self, data: dict):
        new_object = self.model(**data)
        self.session.add(new_object)
        await self.session.commit()
        return new_object

    @no_result_found_handler()
    async def update_one(self, id: int, data: dict):
        query = (
            update(self.model).where(self.model.id == id).values(**data)
        ).returning(self.model.id, self.model.name, self.model.file_url)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.fetchone()

    @no_result_found_handler()
    async def delete_one(self, id: int):
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        obj = result.scalar_one()
        await self.session.delete(obj)
        await self.session.commit()
        return obj.file_url
