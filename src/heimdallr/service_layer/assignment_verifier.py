"""
Assignment Verifier Service
"""
import abc
import concurrent.futures
from itertools import chain

from spacy import Language

from heimdallr.adapters.assignment_reader import AssignmentReader
from heimdallr.adapters.repository import AsyncAssignmentRepository
from heimdallr.domain.commands.assignments import VerifyAssignment
from heimdallr.domain.events.assignments import (
    AssignmentCompared,
    AssignmentVerified,
    SentenceCompared,
)
from heimdallr.domain.models.assignment import Assignment


class AssignmentVerifier(abc.ABC):
    """
    Assignment Verifier Service.

    Verifies if an assignment is plagiarized.
    """

    @abc.abstractmethod
    async def verify(self, command: VerifyAssignment) -> AssignmentVerified:
        """
        Verifies if an assignment is plagiarized.

        Args:
            command (VerifyAssignment): A file reference and its type.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compare_assignments(self, assignment: Assignment, entry: Assignment) -> AssignmentCompared:
        """
        Given a new entry, looks for plagiarism in an assignment.

        Args:
            assignment (Assignment): An assignment.
            entry (Assignment): An assignment to check for plagiarism.

        Returns:
            None: When the assignment is not plagiarized.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compare_sentence(self, sentence: str, entry_sentence: str) -> SentenceCompared:
        """
        Compares two sentences similarities
        .
        Args:
            sentence (str): Sentence from an assignment already persisted.
            entry_sentence (str): Sentence from a new entry to be checked for plagiarism.

        Returns:
            SentenceCompared: A comparison result event.
        """
        raise NotImplementedError


class SpacyAssignmentVerifier(AssignmentVerifier):
    def __init__(
        self,
        reader: AssignmentReader,
        repository: AsyncAssignmentRepository,
        nlp: Language,
        similarity_threshold: float = 0.95,
    ):
        """
        Args:
            reader (AssignmentReader): A file reader.
            repository (AsyncAssignmentRepository): An assignment repository.
            nlp (Language): The Natural Language Processor.
            similarity_threshold (float): The minimum similarity required to consider a sentence plagiarized.
        """
        self.reader = reader
        self.repository = repository
        self.nlp = nlp
        self.similarity_threshold = similarity_threshold

    async def verify(self, command: VerifyAssignment) -> AssignmentVerified:
        # create an assignment from a file
        entry = self.reader.read(command.file_ref, command.file_type)

        if not command.verify or not entry.content:
            return AssignmentVerified(id=entry.id, author=entry.author)

        assignments: list[Assignment] = await self.repository.find_all()
        comparisons: list[AssignmentCompared] = []

        # using concurrent.futures to parallelize the comparisons
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.compare_assignments, assignment, entry) for assignment in assignments]

            for future in concurrent.futures.as_completed(futures):
                result: AssignmentCompared = future.result()
                if result.similarities:
                    comparisons.append(result)

        # for assignment in assignments:
        #     # when an assignment is already persisted, do not compare
        #     if assignment == entry:
        #         return AssignmentVerified(id=assignment.id, author=assignment.author)
        #
        #     result = self.compare_assignments(assignment=assignment, entry=entry)
        #
        #     if result.similarities:
        #         comparisons.append(result)

        persisted = await self.repository.save(entry)

        return AssignmentVerified(
            id=persisted.id,
            title=persisted.title,
            author=persisted.author,
            similarities=comparisons,
        )

    def compare_assignments(self, assignment: Assignment, entry: Assignment) -> AssignmentCompared:
        """
        Given a new entry, looks for plagiarism in an assignment.

        Args:
            assignment (Assignment): An assignment.
            entry (Assignment): An assignment to check for plagiarism.

        Returns:
            None: When the assignment is not plagiarized.
        """
        comparison_results: set[SentenceCompared] = set()

        # flatten the content of the assignment
        sentences: list[str] = list(chain.from_iterable(assignment.content))
        entry_sentences: list[str] = list(chain.from_iterable(entry.content))

        # find the first plagiarized match for each entry sentence
        for entry_sentence in entry_sentences:
            for sentence in sentences:
                result = self.compare_sentence(sentence=sentence, entry_sentence=entry_sentence)
                if result.plagiarism >= self.similarity_threshold:
                    comparison_results.add(self.compare_sentence(sentence=sentence, entry_sentence=entry_sentence))
                    break

        return AssignmentCompared(
            id=assignment.id,
            author=assignment.author,
            similarities=list(comparison_results),
            # pylint: disable=consider-using-generator
            plagiarism=sum([result.plagiarism for result in comparison_results]) / len(entry_sentences),
        )

    def compare_sentence(self, sentence: str, entry_sentence: str) -> SentenceCompared:
        persisted_sentence_doc = self.nlp(sentence)
        entry_sentence_doc = self.nlp(entry_sentence)
        similarity = persisted_sentence_doc.similarity(entry_sentence_doc)

        return SentenceCompared(present=sentence, compared=entry_sentence, plagiarism=similarity)
