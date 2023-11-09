"""
Assignment Verifier Service
"""
import abc
import concurrent.futures
import datetime
import logging

from spacy import Language

from heimdallr.adapters.assignment_reader import AssignmentReader
from heimdallr.adapters.repository import AsyncAssignmentRepository
from heimdallr.domain.commands.assignments import VerifyAssignment
from heimdallr.domain.events.assignments import (
    AssignmentCompared,
    AssignmentVerified,
    SentenceCompared,
)
from heimdallr.domain.models.assignment import Assignment, AssignmentVerification

logger = logging.getLogger("uvicorn.error")

"""
According to https://www.inter-contact.de/en/blog/text-length-languages the AVG letters per word is 5.46 for Spanish

Round it up to 6, and add 1 for the space between words, and we get 7 as the AVG word length.
"""
WORD_AVG_LENGTH = 7
MIN_WORDS = 3
MIN_ASSIGNMENT_SIMILARITY = 0.991


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
        detect_plagiarism: bool = True,
    ):
        """
        Args:
            reader (AssignmentReader): A file reader.
            repository (AsyncAssignmentRepository): An assignment repository.
            nlp (Language): The Natural Language Processor.
            similarity_threshold (float): The minimum similarity required to consider a sentence plagiarized.
            detect_plagiarism (bool): Whether to verify assignments or not.
        """
        self.reader = reader
        self.repository = repository
        self.nlp = nlp
        self.similarity_threshold = similarity_threshold
        self.detect_plagiarism = detect_plagiarism

    async def verify(self, command: VerifyAssignment) -> AssignmentVerified:
        # create an assignment from a file
        entry = self.reader.read(file=command.file)

        if not entry.content:
            return AssignmentVerified(id=command.id, author=entry.author)

        entry.id = command.id
        assignments: list[Assignment] = await self.repository.find_all()
        comparisons: list[AssignmentCompared] = []

        # using concurrent.futures to parallelize the comparisons
        if self.detect_plagiarism:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.compare_assignments, assignment, entry) for assignment in assignments]

                for future in concurrent.futures.as_completed(futures):
                    result: AssignmentCompared = future.result()
                    if result.similarities:
                        comparisons.append(result)
        else:
            logger.warning("Assignment verification is disabled.")

        # map the comparison results to the AssignmentVerification model
        verifications = [AssignmentVerification(**comparison.model_dump()) for comparison in comparisons]
        entry.similarities = verifications

        persisted = await self.repository.save(entry)

        logger.info("Assignment %s verified.", str(persisted.id))

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
        starting_time = datetime.datetime.now()

        # preliminary check to avoid unnecessary comparisons
        entry_doc = self.nlp("".join(entry.content))
        assignment_doc = self.nlp("".join(assignment.content))
        similarity = entry_doc.similarity(assignment_doc)

        if similarity < MIN_ASSIGNMENT_SIMILARITY:
            return AssignmentCompared(id=assignment.id, author=assignment.author, plagiarism=0.0)

        if similarity == 1:
            logger.info("EXACTLY SAME AS %s Assignment(id=%s).", assignment.author, str(assignment.id))
            return AssignmentCompared(id=assignment.id, author=assignment.author, plagiarism=1.0)

        logger.info(
            "Similar(%f) to Assignment(id=%s, author=%s)",
            similarity,
            str(assignment.id),
            assignment.author,
        )

        comparison_results: set[SentenceCompared] = set()

        # find the first plagiarized match for each entry sentence
        for entry_sentence in entry.content:
            for sentence in assignment.content:
                result: SentenceCompared = self.compare_sentence(sentence=sentence, entry_sentence=entry_sentence)
                if result.plagiarism >= self.similarity_threshold:
                    comparison_results.add(result)
                    break

        plagiarism = sum(result.plagiarism for result in comparison_results) / len(entry.content)

        seconds = (datetime.datetime.now() - starting_time).total_seconds()

        logger.info(
            "Finished comparison with Assignment(id=%s, author=%s) in %f seconds.",
            str(assignment.id),
            assignment.author,
            seconds,
        )

        return AssignmentCompared(
            id=assignment.id,
            author=assignment.author,
            similarities=list(comparison_results),
            plagiarism=plagiarism,
        )

    def compare_sentence(self, sentence: str, entry_sentence: str) -> SentenceCompared:
        # assume that the sentence is not plagiarized if it is too short
        if len(sentence) < MIN_WORDS * WORD_AVG_LENGTH:
            return SentenceCompared(present=sentence, compared=entry_sentence, plagiarism=0)

        persisted_sentence_doc = self.nlp(sentence)
        entry_sentence_doc = self.nlp(entry_sentence)
        similarity = persisted_sentence_doc.similarity(entry_sentence_doc)

        return SentenceCompared(present=sentence, compared=entry_sentence, plagiarism=similarity)
