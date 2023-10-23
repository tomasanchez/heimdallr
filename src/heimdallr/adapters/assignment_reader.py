"""
Adapter for reading assignments from a file.
"""
import abc
import datetime
from typing import BinaryIO

import fitz
from spacy import Language

from heimdallr.domain.models.assignment import Assignment, Page
from heimdallr.utils.content_type import APPLICATION_PDF
from heimdallr.utils.formatting import contains_letters_or_numbers, normalize_sentence


class AssignmentReader(abc.ABC):
    @abc.abstractmethod
    def read(self, file_ref: str | BinaryIO, file_type: str) -> Assignment:
        """
        Parses a file into a domain model.

        Args:
            file_ref (str | BinaryIO): Either a file path or a file stream.
            file_type (str): The file type.

        Returns:
            Assignment: A mapped document.
        """
        raise NotImplementedError


class SpacyAssignmentReader(AssignmentReader):
    SPACY_PERSON_LABEL = "PER"

    def __init__(self, nlp: Language, excluded_names: list[str] | None = None):
        """
        A PDF Reader that maps the document into a domain model.

        Args:
            nlp (Language): The Natural Language Processor.
            excluded_names (list[str] | None): A list of names to be excluded from the document.
        """
        if excluded_names is None:
            self.excluded_names = [
                "Dr",
                "Ingeniero",
                "Ing",
                "Licenciado",
                "Lic",
                "MSc",
                "Mg",
                "Profesor",
                "Prof",
                "Hernán Borré",
                "Hernan Borre",
                "Hernan",
                "Borre",
                "Maximiliano Bracho",
                "Maximiliano",
                "Bracho",
            ]
        self.nlp = nlp

    def read(self, file_ref: str | BinaryIO, file_type: str = "pdf") -> Assignment:
        if file_type == APPLICATION_PDF:
            return self.read_pdf(file_ref)

        return Assignment(content=[], date=datetime.date.today(), author="Unknown")

    def read_pdf(self, file_ref: str | BinaryIO) -> Assignment:
        """
        Parses a PDF file into a domain model.

        Args:
            file_ref (str | BinaryIO): Either a file path or a file stream.

        Returns:
            Assignment: A mapped document.
        """
        args: dict[str, str | bytes] = {"filetype": "pdf"}

        if isinstance(file_ref, str):
            args["filename"] = file_ref
        else:
            args["stream"] = file_ref.read()

        file_document = fitz.Document(**args)

        pages: list[Page] = [self._parse_page(page.get_textpage().extractText()) for page in file_document]

        author = self._find_out_author(file_document[0].get_textpage().extractText())

        file_document.close()

        return Assignment(content=pages, date=datetime.date.today(), author=author)

    def _parse_page(self, page_text: str) -> list[str]:
        """
        Parses string from a page into a list of sentences.

        Args:
            page_text: the string to be parsed.

        Returns:
            list[str]: A list of sentences.
        """

        # Parse the page text into a spacy document
        doc = self.nlp(page_text)

        # Split the page text into sentences
        page_sentences = [normalize_sentence(str(s)) for s in doc.sents if contains_letters_or_numbers(str(s))]

        return page_sentences

    def _find_out_author(self, page_text: str) -> str:
        """
        Finds out the author of the assignment.
        It supposes that the document contains a page with the author's name on it.

        Args:
            page_text: The first page of the assignment.

        Returns:
            str: The author's name.
        """

        doc = self.nlp(page_text)

        names = [
            ent.text
            for ent in doc.ents
            if (
                ent.label_ == self.SPACY_PERSON_LABEL
                and not any(ent.text.startswith(name) for name in self.excluded_names)
            )
        ]

        return names[0] if names else "Unknown"