"""
Dependencies for Heimdallr.
"""
from typing import Annotated

import spacy
from fastapi import Depends

from heimdallr.adapters.assignment_reader import AssignmentReader, SpacyAssignmentReader
from heimdallr.adapters.db import ClientFactory
from heimdallr.adapters.motor_repositories import (  # type: ignore[attr-defined]
    MotorAssignmentRepository,
)
from heimdallr.adapters.repository import AsyncAssignmentRepository
from heimdallr.service_layer.assignment_verifier import (
    AssignmentVerifier,
    SpacyAssignmentVerifier,
)
from heimdallr.settings.mongo_settings import MongoSettings

NLP_SPANISH = "es_core_news_lg"

nlp: spacy.Language | None = None

########################################################################################################################
# Database
########################################################################################################################

mongo_settings = MongoSettings()


def get_client_factory() -> ClientFactory:
    """
    Injects a database client factory.
    """

    return ClientFactory(url=mongo_settings.CLIENT)


ClientFactoryDependency = Annotated[ClientFactory, Depends(get_client_factory)]

########################################################################################################################
# NLP
########################################################################################################################


def get_nlp() -> spacy.Language:
    """
    Returns the Natural Language Processor.
    """
    global nlp

    if nlp is None:
        nlp = spacy.load(NLP_SPANISH)

    return nlp


NLPDependency = Annotated[spacy.Language, Depends(get_nlp)]


########################################################################################################################
# Assignment Reader
########################################################################################################################

pdf_assignment_reader: AssignmentReader | None = None


def get_assignment_reader(natural_language_processor: NLPDependency) -> AssignmentReader:
    """
    Returns the Assignment Reader.
    """
    global pdf_assignment_reader

    if pdf_assignment_reader is None:
        pdf_assignment_reader = SpacyAssignmentReader(natural_language_processor)

    return pdf_assignment_reader


AssignmentReaderDependency = Annotated[AssignmentReader, Depends(get_assignment_reader)]

########################################################################################################################
# Assignment Repository
########################################################################################################################

assignment_repository: AsyncAssignmentRepository | None = None


def get_assignment_repository(client_factory: ClientFactoryDependency) -> AsyncAssignmentRepository:
    """
    Returns the Assignment Repository.
    """
    global assignment_repository

    if assignment_repository is None:
        assignment_repository = MotorAssignmentRepository(client=client_factory(), db_name=mongo_settings.DATABASE)

    return assignment_repository


AssignmentRepositoryDependency = Annotated[AsyncAssignmentRepository, Depends(get_assignment_repository)]


########################################################################################################################
# Assignment Verifier
########################################################################################################################

assignment_verifier: AssignmentVerifier | None = None


def get_assignment_verifier(
    reader: AssignmentReaderDependency,
    assignment_repo: AssignmentRepositoryDependency,
    natural_language_processor: NLPDependency,
) -> AssignmentVerifier:
    """
    Returns the Assignment Verifier.
    """
    global assignment_verifier

    if assignment_verifier is None:
        assignment_verifier = SpacyAssignmentVerifier(
            reader=reader, repository=assignment_repo, nlp=natural_language_processor
        )

    return assignment_verifier


AssignmentVerifierDependency = Annotated[AssignmentVerifier, Depends(get_assignment_verifier)]
