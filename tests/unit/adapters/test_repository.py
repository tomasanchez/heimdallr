"""
Test for Repository Module
"""
from heimdallr.domain.models.assignment import BaseDocument
from tests.mocks import InMemRepository


class TestRepositoryModel(BaseDocument):
    foo: str


class TestRepository:
    def test_find_all(self):
        """
        GIVEN a repository
        WHEN find_all is called
        THEN all entities are returned
        """
        # given
        document_1 = TestRepositoryModel(foo="bar")
        repository = InMemRepository(data={document_1.id: document_1})

        # when
        models = repository.find_all()

        # then
        assert document_1 in models

    def test_find_by_id(self):
        """
        GIVEN a repository
        WHEN find_by is called with an id
        THEN the entity is returned
        """
        # given
        document_1 = TestRepositoryModel(foo="bar")
        repository = InMemRepository(data={document_1.id: document_1})

        # when
        model = repository.find_by(id=document_1.id)

        # then
        assert model == document_1

    def test_find_by_id_non_present(self):
        """
        GIVEN a repository
        WHEN find_by is called with an id that does not exist
        THEN None is returned
        """
        # given
        document_1 = TestRepositoryModel(foo="bar")
        repository = InMemRepository(data={document_1.id: document_1})

        # when
        model = repository.find_by(id="non-present")

        # then
        assert model is None

    def test_save(self):
        """
        GIVEN a repository
        WHEN save is called with an entity
        THEN the entity is saved
        """
        # given
        document_1 = TestRepositoryModel(foo="bar")
        repository = InMemRepository()

        # when
        repository.save(document_1)

        # then
        assert repository.find_by(id=document_1.id) == document_1

    def test_delete(self):
        """
        GIVEN a repository
        WHEN delete is called with an entity
        THEN the entity is deleted
        """
        # given
        document_1 = TestRepositoryModel(foo="bar")
        repository = InMemRepository(data={document_1.id: document_1})

        # when
        repository.delete(document_1)

        # then
        assert repository.find_by(id=document_1.id) is None
