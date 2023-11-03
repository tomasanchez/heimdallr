"""
Adapter for reading assignments from a file.
"""
import abc
import datetime
import os
import tempfile
from io import BytesIO
from itertools import dropwhile

import docx
import fitz
import pytextract
from fastapi import UploadFile
from spacy import Language

from heimdallr.domain.models.assignment import Assignment
from heimdallr.utils import content_type
from heimdallr.utils.formatting import contains_letters_or_numbers, normalize_sentence


class AssignmentReader(abc.ABC):
    @abc.abstractmethod
    def read(self, file: UploadFile) -> Assignment:
        """
        Parses a file into a domain model.

        Args:
            file (UploadFile): The file to be parsed.
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

    def read(self, file: UploadFile) -> Assignment:
        if file.content_type == content_type.APPLICATION_PDF:
            return self.read_pdf(file)

        if file.content_type == content_type.APPLICATION_DOCX:
            return self.read_docx(file)

        if file.content_type == content_type.APPLICATION_WORD:
            return self.read_msword(file)

        return Assignment(content=[], date=datetime.date.today(), author="Unknown", title=file.filename)

    def read_pdf(self, file: UploadFile) -> Assignment:
        """
        Parses a PDF file into a domain model.

        Args:
            file: The file to be parsed.

        Returns:
            Assignment: A mapped document.
        """
        file_document = fitz.Document(stream=file.file.read(), filetype="pdf")

        pages: list[list[str]] = [self._parse_page(page.get_textpage().extractText()) for page in file_document]

        author = self._find_out_author(file_document[0].get_textpage().extractText())

        file_document.close()

        return Assignment(
            author=author,
            title=file.filename,
            content=[sentence for page in pages for sentence in page],
            date=datetime.date.today(),
        )

    def read_docx(self, file: UploadFile) -> Assignment:
        """
        Parses a DOCX file into a domain model.

        Args:
            file (UploadFile): a file reference.

        Returns:
            Assignment: A mapped document.
        """
        # obtain the file as a stream compatible with python-docx Document
        bytes_io = BytesIO()
        bytes_io.write(file.file.read())

        doc = docx.Document(bytes_io)

        paragraphs = [p.text for p in doc.paragraphs if contains_letters_or_numbers(p.text)]

        content = [sentence for paragraph in paragraphs for sentence in self._parse_page(paragraph)]

        maybe_authors = [self._find_out_author(paragraph) for paragraph in paragraphs]

        author = next(dropwhile(lambda name: name == "Unknown", maybe_authors), "Unknown")

        return Assignment(
            author=author,
            title=file.filename,
            content=content,
            date=datetime.date.today(),
        )

    def read_msword(self, file: UploadFile) -> Assignment:
        """
        Parses a .doc file into a domain model.

        Args:
            file (UploadFile): a file reference.

        Returns:
            Assignment: A mapped document.
        """

        # create a temporary file with a specific name
        with tempfile.NamedTemporaryFile(delete=False, prefix="temp_doc_", suffix=".doc") as temp_file:
            temp_file.write(file.file.read())

        text = pytextract.process(temp_file.name, extension="doc")

        content = list(self._parse_page(text)) if text else []

        maybe_authors = list(self._find_out_author(sentence) for sentence in content) if text else []

        author = next(dropwhile(lambda name: name == "Unknown", maybe_authors), "Unknown")

        temp_file.close()
        os.remove(temp_file.name)

        return Assignment(
            author=author,
            title=file.filename,
            content=content,
        )

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
