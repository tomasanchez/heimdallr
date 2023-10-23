"""
Assignments events.
"""
from pydantic import UUID4, Field

from heimdallr.domain.schemas import CamelCaseModel


class SentenceCompared(CamelCaseModel):
    """
    Sentence compared event.
    """

    present: str = Field(description="Present sentence.", example="This is the already present sentence.")
    compared: str = Field(description="Compared sentence.", example="This is the new sentences evaluated.")
    plagiarism: float = Field(description="Plagiarism percentage.", example=0.0, default=0.0)


class AssignmentCompared(CamelCaseModel):
    """
    Assignment compared event.
    """

    id: UUID4 = Field(description="Assigment Compared ID.", example="123e4567-e89b-12d3-a456-426614174000")
    author: str | None = Field(description="Assignment's author.", example="John Doe", default="Unknown")
    plagiarism: float = Field(description="Average Plagiarism percentage.", example=0.0, default=0.0)
    similarities: list[SentenceCompared] = Field(description="Similarities found.", example=[], default_factory=list)


class AssignmentVerified(CamelCaseModel):
    """
    Assignment verified event.
    """

    id: UUID4 = Field(description="Assignment's ID.", example="123e4567-e89b-12d3-a456-426614174000")
    title: str | None = Field(description="Assignment's title.", example="NLP Assignment", default="Unknown")
    author: str | None = Field(description="Name of the responsible person", example="John Doe", default="Unknown")
    similarities: list[AssignmentCompared] = Field(description="Plagiarism results.", example=[], default_factory=list)


class AssignmentStored(CamelCaseModel):
    """
    Assignment stored event.
    """

    id: UUID4 = Field(description="Assignment's ID.", example="123e4567-e89b-12d3-a456-426614174000")
    title: str | None = Field(description="Assignment's title.", example="NLP Assignment", default="Unknown")
    author: str | None = Field(description="Name of the responsible person", example="John Doe", default="Unknown")
    content: list[list[str]] = Field(description="Assignment's content.", example=[["This is a sentence."]])