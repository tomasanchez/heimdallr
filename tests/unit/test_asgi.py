"""
Test suite for ASGI Application
"""
import pytest

from heimdallr.asgi import get_application, lifespan


class TestASGI:
    """
    Unit test suite for ASGI Application
    """

    def test_get_application(self):
        """
        GIVEN a FastAPI application
        WHEN the application is initialized
        THEN the application is returned
        """
        assert get_application() is not None

    @pytest.mark.asyncio
    async def test_lifespan(self):
        """
        GIVEN a FastAPI application
        WHEN the lifespan is called
        THEN the NLP is initialized
        """

        # given
        app = get_application()

        # when
        async with lifespan(app=app):
            # then does not fail
            pass
