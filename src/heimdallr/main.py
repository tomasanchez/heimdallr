"""
Applicant Main File.
"""
from fastapi import FastAPI

from heimdallr.asgi import get_application

app: FastAPI = get_application()

if __name__ == "__main__":
    # pylint: disable=wrong-import-position
    import uvicorn

    import heimdallr.settings.uvicorn_settings

    settings = heimdallr.UvicornSettings()

    uvicorn.run(
        "heimdallr.main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD,
    )
