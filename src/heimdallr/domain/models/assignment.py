"""
Assignment.
"""
import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

Sentence = str

Page = list[Sentence]


class BaseDocument(BaseModel):
    """
    Convenience mapped superclass for all documents to be persisted in a consistent manner.

    Attributes:
        id (UUID): The document ID.
    """

    id: UUID = Field(default_factory=uuid4, alias="_id", title="Document ID")

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


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
    author: str = "Unknown"
    content: list[Page]
    date: datetime.date | None = None
