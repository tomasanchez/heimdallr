"""
Assignments events.
"""
from uuid import uuid4

from pydantic import UUID4, Field

from heimdallr.domain.models.assignment import UNKNOWN_AUTHOR, Topic
from heimdallr.domain.schemas import CamelCaseModel


class SentenceCompared(CamelCaseModel):
    """
    Sentence compared event.
    """

    present: str = Field(description="Present sentence.", example="This is the already present sentence.")
    compared: str = Field(description="Compared sentence.", example="This is the new sentences evaluated.")
    plagiarism: float = Field(description="Plagiarism percentage.", example=0.0, default=0.0)

    def __hash__(self):
        return hash((self.present, self.compared, self.plagiarism))

    def __eq__(self, other):
        return (
            isinstance(other, SentenceCompared)
            and self.present == other.present
            and self.compared == other.compared
            and self.plagiarism == other.plagiarism
        )


class AssignmentCompared(CamelCaseModel):
    """
    Assignment compared event.
    """

    id: UUID4 = Field(description="Assigment Compared ID.", example="123e4567-e89b-12d3-a456-426614174000")
    author: str | None = Field(description="Assignment's author.", example="John Doe", default=UNKNOWN_AUTHOR)
    topic: Topic = Field(description="Assignment's topic.", example="NLP", default=Topic.UNDEFINED)
    plagiarism: float = Field(description="Average Plagiarism percentage.", example=0.0, default=0.0)
    similarities: list[SentenceCompared] = Field(description="Similarities found.", example=[], default_factory=list)


class AssignmentVerified(CamelCaseModel):
    """
    Assignment verified event.
    """

    id: UUID4 = Field(description="Assignment's ID.", example="123e4567-e89b-12d3-a456-426614174000")
    title: str | None = Field(description="Assignment's title.", example="NLP Assignment", default="Unknown")
    author: str | None = Field(description="Name of the responsible person", example="John Doe", default=UNKNOWN_AUTHOR)
    similarities: list[AssignmentCompared] | None = Field(description="Plagiarism results.", example=[], default=None)


class AssignmentStored(CamelCaseModel):
    """
    Assignment stored event.
    """

    id: UUID4 = Field(description="Assignment's ID.", example="123e4567-e89b-12d3-a456-426614174000")
    title: str | None = Field(description="Assignment's title.", example="NLP Assignment", default="Unknown")
    author: str | None = Field(description="Name of the responsible person", example="John Doe", default=UNKNOWN_AUTHOR)
    topic: Topic = Field(description="Assignment's topic.", example="NLP", default=Topic.UNDEFINED)
    content: list[str] = Field(description="Assignment's content.", example=[["This is a sentence."]])


class JobScheduled(CamelCaseModel):
    """
    Job scheduled event.
    """

    id: UUID4 = Field(description="Job's ID.", example="123e4567-e89b-12d3-a466-426614174000", default_factory=uuid4)
    message: str = Field(description="Job's message.", example="Job scheduled.")
