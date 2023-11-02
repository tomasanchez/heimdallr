"""
Database connection
"""

from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient | None = None  # type: ignore[valid-type]


class ClientFactory:
    """
    Database connection factory
    """

    def __init__(self, url):
        global client

        if not client:
            client = AsyncIOMotorClient(url, uuidRepresentation="standard")

        self._client = client

    def __call__(self, *args, **kwargs):
        """
        Get database client
        """
        return self._client
