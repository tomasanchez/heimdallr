"""
Commands Related to Assignments
"""
from dataclasses import dataclass
from uuid import uuid4

from fastapi import UploadFile
from pydantic import UUID4, Field


@dataclass
class VerifyAssignment:
    """
    Verify Assignment Command.
    """

    # pylint: disable=invalid-name
    id: UUID4 = Field(description="UUID", example="123e4567-e89b-12d3-a456-426614174000", default_factory=uuid4)
    file: UploadFile = Field(description="Assignment's File")
