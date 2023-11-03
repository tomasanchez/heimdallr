"""
Events related to the monitoring of the application.
"""
from enum import Enum
from typing import Literal

from pydantic import Field

from heimdallr.domain.schemas import CamelCaseModel


class ServiceStatus(str, Enum):
    """Service status enumeration.

    Attributes:
        ONLINE (str): Service is online.
        OFFLINE (str): Service is offline.
    """

    ONLINE = "READY"
    OFFLINE = "ERROR"


class LivenessProbed(CamelCaseModel):
    """
    Event that is sent when the application is probed for liveness.
    """

    status: Literal["Ok", "Error"] = Field(
        description="The status of the application.",
        default="Ok",
    )


class ServiceProbed(CamelCaseModel):
    """
    Event description when a service status is verified.
    """

    name: str = Field(description="Service identifier", examples=["DB"])
    status: ServiceStatus = Field(description="Availability", default=ServiceStatus.ONLINE)
    detail: str | dict | None = Field(description="Status description", examples=["Credentials expired"], default=None)


class ReadinessProbed(CamelCaseModel):
    """
    Event that is sent when the application is probed for readiness.
    """

    name: str = Field(description="The name of the service.", examples=["API", "DB"])
    status: ServiceStatus = Field(description="The readiness probe of the application.", default=ServiceStatus.ONLINE)
    services: list[ServiceProbed] | None = Field(description="Dependencies status", default=None)
