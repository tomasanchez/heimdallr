"""
Dependencies for Heimdallr.
"""
import logging
import os
from typing import Annotated

import spacy
from fastapi import Depends

from heimdallr.adapters.assignment_reader import (
    AssignmentReader,
    SklearnTopicPredictor,
    SpacyAssignmentReader,
    TopicPredictor,
)
from heimdallr.adapters.db import ClientFactory
from heimdallr.adapters.motor_repositories import (  # type: ignore[attr-defined]
    MotorAssignmentRepository,
)
from heimdallr.adapters.repository import AsyncAssignmentRepository
from heimdallr.service_layer.assignment_verifier import (
    AssignmentVerifier,
    SpacyAssignmentVerifier,
)
from heimdallr.settings.api_settings import ApplicationSettings
from heimdallr.settings.mongo_settings import MongoSettings

logger = logging.getLogger("uvicorn.error")

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
topic_predictor: TopicPredictor | None = None

pdf_assignment_reader: AssignmentReader | None = None


def get_topic_predictor(natural_language_processor: NLPDependency) -> TopicPredictor | None:
    """
    Returns the Topic Predictor.
    """
    global topic_predictor

    if topic_predictor is None:
        model_path = ApplicationSettings().MODEL_PATH
        if os.path.exists(model_path):
            logger.info("Loading model from %s.", model_path)
            topic_predictor = SklearnTopicPredictor(
                nlp=natural_language_processor,
                download=True,
                model_path=model_path,
            )
        else:
            logger.warning("Model not found at %s.", model_path)

    return topic_predictor


TopicPredictorDependency = Annotated[TopicPredictor | None, Depends(get_topic_predictor)]


def get_assignment_reader(
    natural_language_processor: NLPDependency,
    predictor: TopicPredictorDependency,
) -> AssignmentReader:
    """
    Returns the Assignment Reader.
    """
    global pdf_assignment_reader

    if pdf_assignment_reader is None:
        pdf_assignment_reader = SpacyAssignmentReader(nlp=natural_language_processor, topic_predictor=predictor)

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
        settings = ApplicationSettings()
        assignment_verifier = SpacyAssignmentVerifier(
            reader=reader,
            repository=assignment_repo,
            nlp=natural_language_processor,
            similarity_threshold=settings.SIMILARITY_THRESHOLD,
            detect_plagiarism=settings.DETECT_PLAGIARISM,
        )

    return assignment_verifier


AssignmentVerifierDependency = Annotated[AssignmentVerifier, Depends(get_assignment_verifier)]
