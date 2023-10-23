"""
Assignments Entry Point.
"""
import logging
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Path, UploadFile, status
from pydantic import UUID4

from heimdallr.dependencies import (
    AssignmentRepositoryDependency,
    AssignmentVerifierDependency,
)
from heimdallr.domain.commands.assignments import VerifyAssignment
from heimdallr.domain.events.assignments import AssignmentStored, AssignmentVerified
from heimdallr.domain.schemas import ResponseModel
from heimdallr.utils import content_type

router = APIRouter(prefix="/assignments")

supported_content_types = [
    content_type.APPLICATION_PDF,
    content_type.APPLICATION_WORD,
    content_type.APPLICATION_DOCX,
]


@router.post(path="", status_code=status.HTTP_200_OK, tags=["Commands"])
async def verify_assignment(
    verification_service: AssignmentVerifierDependency,
    file: Annotated[UploadFile, File(description="Assignment's File")],
) -> ResponseModel[AssignmentVerified]:
    """
    Compares an assignment against a set of other assignments to see if there is any plagiarism.

    Only PDF, DOC and DOCX files are supported.
    """
    logging.info("Verify assignment.")

    # checks if the file type is supported
    if file.content_type not in supported_content_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Content type {file.content_type} is not supported.",
        )

    # creates a command to be handled by the service
    command = VerifyAssignment(
        file_ref=file.file,
        file_type=file.content_type,  # file.content_type,
    )

    # calls the service - which will produce an event
    event = await verification_service.verify(command=command)

    return ResponseModel(data=event)


async def get_assignment(
    assignment_id: Annotated[
        UUID4, Path(description="Assignment's ID", example="123e4567-e89b-12d3-a456-426614174000")
    ],
    repository: AssignmentRepositoryDependency,
) -> ResponseModel[AssignmentStored]:
    """
    Returns an assignment by ID.
    """
    logging.info("Get assignment.")
    model = await repository.find_by_id(assignment_id)

    event = AssignmentStored(**model.dict())

    return ResponseModel(data=event)


@router.get(path="", status_code=status.HTTP_200_OK, tags=["Queries"])
async def get_assignments(
    repository: AssignmentRepositoryDependency,
) -> ResponseModel[list[AssignmentStored]]:
    """
    Returns all assignments.
    """
    logging.info("Get assignments.")
    models = await repository.find_all()

    events = [AssignmentStored(**model.dict()) for model in models]

    return ResponseModel[list[AssignmentStored]](data=events)
