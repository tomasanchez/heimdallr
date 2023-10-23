from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from heimdallr.adapters.repository import (
    T,
    AsyncReadOnlyRepository,
    AsyncWriteOnlyRepository,
    AsyncAssignmentRepository,
)
from heimdallr.domain.models.assignment import Assignment


class MotorRepositoryMixin:
    """
    Mixin class for motor repositories.
    """

    def __init__(self, client: AsyncIOMotorClient, db_name: str, model_factory: type[T]):
        """

        Args:
            client: Motor Client
            db_name: Name of the database
        """
        self.collection_name = model_factory.__name__.lower()
        self.collection: AsyncIOMotorCollection = client.get_database(db_name).get_collection(self.collection_name)
        self.model_factory = model_factory

    def to_model(self, document: dict | None) -> T | None:
        """
        Convert a document to a model.

        Args:
            document (dict| None): Document to be converted.

        Returns:
            T: Model instance.
        """

        return self.model_factory(**document) if document else None

    @staticmethod
    def to_document(model: T) -> dict:
        """
        Convert a model to a document.

        Args:
            model: Model to be converted.

        Returns:
            dict: Document instance.
        """

        return model.model_dump(mode="json")


class MotorReadOnlyRepository(AsyncReadOnlyRepository, MotorRepositoryMixin):
    """
    Motor read-only repository generic implementation.
    """

    async def find_by(self, *args, **kwargs) -> T | None:
        entry = await self.collection.find_one(kwargs)

        return self.to_model(entry)

    async def find_all(self, *args, **kwargs) -> list[T]:
        cursor = self.collection.find(kwargs)

        entries: list[T] = list()

        async for entry in cursor:
            entries.append(self.to_model(entry))

        return entries


class MotorWriteOnlyRepository(AsyncWriteOnlyRepository, MotorRepositoryMixin):
    async def save(self, entity: T, *args, **kwargs) -> T:
        entry = jsonable_encoder(entity)
        await self.collection.insert_one(entry)
        return entity

    async def delete(self, entity: T, *args, **kwargs) -> None:
        await self.collection.delete_one({"_id": entity.id})


class MotorAssignmentRepository(AsyncAssignmentRepository, MotorWriteOnlyRepository, MotorReadOnlyRepository):
    """
    Motor repository implementation for Assignment.
    """

    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        super().__init__(client, db_name, Assignment)
