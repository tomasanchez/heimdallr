"""
Pytest Fixtures.
"""
import pytest
from spacy import Language
from starlette.testclient import TestClient

from heimdallr.adapters.assignment_reader import AssignmentReader, SpacyAssignmentReader
from heimdallr.adapters.repository import AsyncAssignmentRepository
from heimdallr.dependencies import get_nlp
from heimdallr.main import app
from heimdallr.service_layer.assignment_verifier import (
    AssignmentVerifier,
    SpacyAssignmentVerifier,
)
from tests.mocks import AsyncInMemAssignmentRepository


@pytest.fixture(name="test_client")
def fixture_test_client() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Returns:
        TestClient: A test client for the app.
    """
    return TestClient(app)


@pytest.fixture(name="assignment_repository")
def fixture_assignment_repository() -> AsyncAssignmentRepository:
    """
    Create an assignment repository.
    """
    return AsyncInMemAssignmentRepository()


@pytest.fixture(name="nlp")
def fixture_nlp() -> Language:
    """
    Injects a Natural Language Processor.
    """
    return get_nlp()


@pytest.fixture(name="assignment_reader")
def fixture_assignment_reader(nlp) -> AssignmentReader:
    """
    Create an assignment service.
    """
    return SpacyAssignmentReader(nlp=nlp)


@pytest.fixture(name="assignment_verifier")
def fixture_assignment_service(nlp, assignment_reader, assignment_repository) -> AssignmentVerifier:
    """
    Injects an assignment service.
    """
    return SpacyAssignmentVerifier(nlp=nlp, reader=assignment_reader, repository=assignment_repository)
