"""
Assignments Entry Point.
"""
import logging
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    HTTPException,
    Path,
    UploadFile,
    status,
)
from pydantic import UUID4

from heimdallr.dependencies import (
    AssignmentRepositoryDependency,
    AssignmentVerifierDependency,
)
from heimdallr.domain.commands.assignments import VerifyAssignment
from heimdallr.domain.events.assignments import (
    AssignmentStored,
    AssignmentVerified,
    JobScheduled,
)
from heimdallr.domain.models.assignment import Assignment
from heimdallr.domain.schemas import ResponseModel
from heimdallr.utils import content_type

router = APIRouter(prefix="/assignments")

supported_content_types = [
    content_type.APPLICATION_PDF,
    content_type.APPLICATION_WORD,
    content_type.APPLICATION_DOCX,
]


@router.post(path="", status_code=status.HTTP_202_ACCEPTED, tags=["Commands"])
async def verify_assignment(
    verification_service: AssignmentVerifierDependency,
    file: Annotated[UploadFile, File(description="Assignment's File")],
    background_tasks: BackgroundTasks,
) -> ResponseModel[JobScheduled]:
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

    # generate job
    job = JobScheduled(
        message="Assignment verification scheduled. Once completed, similarities will be shown when retrieved by id.",
    )

    # creates a command to be handled by the service
    command = VerifyAssignment(
        id=job.id,
        file=file,
    )

    # calls the service - which will produce an event
    background_tasks.add_task(verification_service.verify, command=command)

    return ResponseModel(data=job)


@router.get(path="", status_code=status.HTTP_200_OK, tags=["Queries"])
async def get_assignments(
    repository: AssignmentRepositoryDependency,
) -> ResponseModel[AssignmentStored]:
    """
    Returns all assignments.
    """
    logging.info("Get assignments.")
    models: list[Assignment] = await repository.find_all()

    events = [AssignmentStored(**model.model_dump()) for model in models]

    return ResponseModel[AssignmentStored](data=events)


@router.get(path="/{assignment_id}", status_code=status.HTTP_200_OK, tags=["Queries"])
async def get_assignment_by_id(
    assignment_id: Annotated[
        UUID4, Path(description="Assignment's ID", examples=["db5f72ab-23ce-4087-ab98-548775184f8e"])
    ],
    repository: AssignmentRepositoryDependency,
) -> ResponseModel[AssignmentVerified]:
    """
    Returns an assignment by ID.
    """

    model: Assignment | None = await repository.find_by(id=assignment_id)  # type: ignore[func-returns-value]

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with id {assignment_id} not found.",
        )

    event = AssignmentVerified(**model.dict())

    return ResponseModel(data=event)
