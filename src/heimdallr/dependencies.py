"""
Dependencies for Heimdallr.
"""
from typing import Annotated

import spacy
from fastapi import Depends

from heimdallr.adapters.assignment_reader import AssignmentReader, SpacyAssignmentReader

NLP_SPANISH = "es_core_news_lg"

nlp: spacy.Language | None = None


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
