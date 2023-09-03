"""
Applicant Main File.
"""
from fastapi import FastAPI

from heimdallr.asgi import get_application

app: FastAPI = get_application()

if __name__ == "__main__":
    # pylint: disable=wrong-import-position
    import uvicorn

    # pylint: disable=ungrouped-imports
    from heimdallr.settings import uvicorn_settings

    settings = uvicorn_settings.UvicornSettings()

    uvicorn.run(
        "heimdallr.main:app",
        host=str(settings.HOST),
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD,
    )
