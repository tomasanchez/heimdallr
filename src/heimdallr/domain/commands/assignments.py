"""
Commands Related to Assignments
"""
from dataclasses import dataclass
from typing import BinaryIO
from uuid import uuid4

from pydantic import UUID4, Field


@dataclass
class VerifyAssignment:
    """
    Verify Assignment Command.
    """

    # pylint: disable=invalid-name
    id: UUID4 = Field(description="UUID", example="123e4567-e89b-12d3-a456-426614174000", default_factory=uuid4)
    file_ref: str | BinaryIO = Field(description="Either a file path or a Binary", example="path/to/file.pdf")
    file_type: str = Field(description="File type.", example="pdf", default="pdf")
    verify: bool = Field(description="Verify the assignment.", example=True, default=True)
