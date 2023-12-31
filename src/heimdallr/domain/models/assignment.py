"""
Assignment.
"""
import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import UUID4, BaseModel, ConfigDict, Field

UNKNOWN_AUTHOR = "Unknown"


class BaseDocument(BaseModel):
    """
    Convenience mapped superclass for all documents to be persisted in a consistent manner.

    Attributes:
        id (UUID): The document ID.
    """

    id: UUID = Field(default_factory=uuid4, alias="_id", title="Document ID")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class Topic(str, Enum):
    """
    Classifies the main topic of an assignment.

    See Also:
        https://www.cosmicpython.com/blog/2020-10-27-i-hate-enums.html
    """

    UNDEFINED = "Undefined"
    EXPERIENCE_ECONOMY = "Experience Economy"
    EMERGING_SYSTEMS = "Emerging Systems"
    DIGITAL_ECONOMY = "Digital Economy"
    INNOVATION = "Innovation"

    def __str__(self) -> str:
        return str.__str__(self)


class ComparisonResult(BaseModel):
    """
    A comparison result.

    Attributes:
        present (str): stored sentence.
        compared (str): assignment sentence.
        plagiarism (float): plagiarism percentage.
    """

    present: str
    compared: str
    plagiarism: float


class AssignmentVerification(BaseModel):
    """
    A comparison result.

    Attributes:
        id (UUID): The compared Assignment ID.
        author (str): The compared Assignment Author.
        plagiarism (float): plagiarism percentage.
        similarities (list[ComparisonResult]): The comparison results.
    """

    id: UUID4
    author: str | None = UNKNOWN_AUTHOR
    plagiarism: float
    similarities: list[ComparisonResult] = []


class Assignment(BaseDocument):
    """
    Represents an Academic Assignment.

    Attributes:
        title (str): The title of the assignment.
        author (str): Name of the author of the assignment.
        content (list[Page]): Pages of paragraphs.
        date (datetime.date): Issue date of the assignment.
    """

    title: str = "Unknown"
    author: str = UNKNOWN_AUTHOR
    topic: Topic = Topic.UNDEFINED
    content: list[str]
    date: datetime.date | None = None
    similarities: list[AssignmentVerification] | None = None

    def __eq__(self, other) -> bool:
        """
        Compares two assignments.

        Args:
            other:

        Returns:
            true when the same author submits the same content.

        """
        if other is None:
            return False

        if not isinstance(other, Assignment):
            return False

        if self.author != other.author:
            return False

        return self.content == other.content
