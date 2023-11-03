"""Monitor entrypoint.

Responsible for probing the system liveness and readiness.
"""

from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from starlette.responses import RedirectResponse

from heimdallr.dependencies import ClientFactoryDependency
from heimdallr.domain.events.monitor import (
    LivenessProbed,
    ReadinessProbed,
    ServiceProbed,
    ServiceStatus,
)
from heimdallr.domain.schemas import ResponseModel

router = APIRouter()


@router.get(
    "/liveness",
    tags=["Monitor"],
    name="Liveness",
    status_code=status.HTTP_200_OK,
)
async def query_liveness_probe() -> ResponseModel[LivenessProbed]:
    """
    Probe the system liveness.

    When working with Kubernetes, Checks if the application within the pod is running and responsive. If the liveness
    probe fails, Kubernetes might restart the pod to recover from unresponsive states.
    """
    return ResponseModel(data=LivenessProbed())


@router.get(
    "/readiness",
    tags=["Monitor"],
    name="Readiness",
    status_code=status.HTTP_200_OK,
)
async def query_readiness_probe(mongo_client_factory: ClientFactoryDependency) -> ResponseModel[ReadinessProbed]:
    """
    Probe the system readiness.

    When working with Kubernetes, Checks if the pod is ready to handle incoming traffic and requests. If the
     readiness probe fails, Kubernetes temporarily stops sending traffic to the pod.
    """
    # check dependant services
    db_status = await _ping_database(client=mongo_client_factory())

    dependencies = [db_status]

    api_status = (
        ServiceStatus.OFFLINE
        if any(dependency.status == "Error" for dependency in dependencies)
        else ServiceStatus.ONLINE
    )

    readiness_probed = ReadinessProbed(
        name="Heimdallr API",
        services=dependencies,
        status=api_status,
    )

    if readiness_probed.status == ServiceStatus.OFFLINE:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=readiness_probed.model_dump())

    return ResponseModel(data=readiness_probed)


@router.get("/", status_code=status.HTTP_301_MOVED_PERMANENTLY, include_in_schema=False)
def root_redirect():
    """
    Redirect to the API documentation.
    """
    return RedirectResponse(url="/docs", status_code=status.HTTP_301_MOVED_PERMANENTLY)


async def _ping_database(client: AsyncIOMotorClient) -> ServiceProbed:  # type: ignore[valid-type]
    """
    Pings the database.

    Args:
        client (MongoClient): The database client.

    Returns:
        StatusChecked: The status of the database.
    """
    service_status = ServiceStatus.ONLINE
    detail = None

    try:
        await client.admin.command("ping")  # type: ignore[attr-defined]
    except ConnectionFailure as cfe:
        service_status = ServiceStatus.OFFLINE
        detail = str(cfe)

    return ServiceProbed(name="MongoDB", status=service_status, detail=detail)
