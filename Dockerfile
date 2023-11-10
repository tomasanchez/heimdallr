FROM python:3.11.4-slim AS development_build

ARG APP_DIR=/app

ARG ENV

ENV ENV=${ENV} \
    PYTHOPNUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1 \
    FASTAPI_MODEL_PATH=/app/models/topic_predictor_dev.joblib \
    UVICORN_PORT=8000   \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_RELOAD=0

# Deploy application
WORKDIR $APP_DIR
COPY pyproject.toml poetry.lock README.md ${APP_DIR}/
COPY db/training.csv ${APP_DIR}/db/
RUN mkdir -p ${APP_DIR}/models
ADD src ${APP_DIR}/src

# System dependencies
RUN apt-get update -y
RUN apt-get install -y antiword
RUN pip install --disable-pip-version-check "poetry==$POETRY_VERSION"

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --only main \
    && poetry run spacy download es_core_news_lg

# train the model
RUN poetry run python -m heimdallr.train

CMD ["poetry", "run", "python","-m", "heimdallr.main"]