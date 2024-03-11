from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def get_one(self, id: int):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def create_one(self, data: dict):
        pass

    @abstractmethod
    async def update_one(self, id: int, data: dict):
        pass

    @abstractmethod
    async def delete_one(self, id: int):
        pass
