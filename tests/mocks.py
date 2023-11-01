"""
Mocks Class for Testing
"""
# mypy: ignore-errors

from uuid import UUID

from heimdallr.adapters.repository import (
    AsyncAssignmentRepository,
    AsyncRepository,
    ReadOnlyRepository,
    T,
    WriteOnlyRepository,
)


class InMemRepository(WriteOnlyRepository, ReadOnlyRepository):
    """
    In-memory repository implementation for testing.
    """

    def __init__(self, data: dict | None = None):
        self._data: dict[UUID, T] = data or {}

    def delete(self, entity: T, *args, **kwargs) -> None:
        if entity.id in self._data:
            del self._data[entity.id]

    def find_all(self, *args, **kwargs) -> list[T]:
        return list(self._data.values())

    def find_by(self, *args, **kwargs) -> T | None:
        return self._data.get(kwargs.get("id"))

    def save(self, entity: T, *args, **kwargs) -> T:
        self._data[entity.id] = entity
        return entity.model_copy(deep=True)


class AsyncInMemRepository(AsyncRepository):
    """
    In-memory Async repository implementation for testing.
    """

    def __init__(self, data: dict | None = None):
        self._data: dict[UUID, T] = data or {}

    async def delete(self, entity: T, *args, **kwargs) -> None:
        if entity.id in self._data:
            del self._data[entity.id]

    async def find_all(self, *args, **kwargs) -> list[T]:
        return list(self._data.values())

    async def find_by(self, *args, **kwargs) -> T | None:
        return self._data.get(kwargs.get("id"))

    async def save(self, entity: T, *args, **kwargs) -> T:
        self._data[entity.id] = entity
        return entity.model_copy(deep=True)


class AsyncInMemAssignmentRepository(AsyncAssignmentRepository, AsyncInMemRepository):
    pass
