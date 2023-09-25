"""
This module abstracts the Database layer with a Repository pattern.
"""
import abc
from typing import TypeVar

from heimdallr.domain.models.assignment import BaseDocument

T = TypeVar("T", bound=BaseDocument)


class ReadOnlyRepository(abc.ABC):
    """
    Abstract base class for read-only repository implementations.
    """

    @abc.abstractmethod
    def find_all(self, *args, **kwargs) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T] : A list of entities.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, *args, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError


class WriteOnlyRepository(abc.ABC):
    """
    Abstract base class for write-only repository implementations.
    """

    @abc.abstractmethod
    def save(self, entity: T, *args, **kwargs) -> T:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: T, *args, **kwargs) -> None:
        """
        Deletes an entity from the repository.

        Args:
            entity (T): The entity to delete.
        """
        raise NotImplementedError


class AsyncReadOnlyRepository(abc.ABC):
    """
    Abstract base class for asynchronous read-only repository implementations.
    """

    @abc.abstractmethod
    async def find_all(self, *args, **kwargs) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T] : A list of entities.

        """
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by(self, *args, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError


class AsyncWriteOnlyRepository(abc.ABC):
    """
    Abstract base class for asynchronous write-only repository implementations.
    """

    @abc.abstractmethod
    async def save(self, entity: T, *args, **kwargs) -> T:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, entity: T, *args, **kwargs) -> None:
        """
        Deletes an entity from the repository.

        Args:
            entity (T): The entity to delete.
        """
        raise NotImplementedError


class AsyncRepository(AsyncWriteOnlyRepository, AsyncReadOnlyRepository, abc.ABC):
    """
    Abstract base class for asynchronous repository implementations.
    """


class AsyncAssignmentRepository(AsyncRepository, abc.ABC):
    """
    Abstract Base Class for Assignment Repository implementations.
    """
