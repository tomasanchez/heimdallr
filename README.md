# Heimdallr

A powerful and intelligent plagiarism detection system designed to uphold academic integrity and ensure the authenticity
of written works. Named after Heimdallr, the all-seeing Norse god, this system possesses unparalleled vigilance and a
watchful eye over the realm of academic content.

More information [Heimdallr](Heimdallr.pdf).

## Content

<!-- TOC -->

* [Heimdallr](#heimdallr)
    * [Content](#content)
    * [Key Features](#key-features)
    * [Why Heimdallr?](#why-heimdallr)
    * [Environment Variables](#environment-variables)
    * [Continuous Integration](#continuous-integration)
    * [Quick set up](#quick-set-up)
    * [Development Environment](#development-environment)
        * [Installing Poetry](#installing-poetry)
        * [Building the Development Environment](#building-the-development-environment)
    * [Running Local](#running-local)
        * [MSWord Document Support](#msword-document-support)
        * [Using Docker (Recommended)](#using-docker-recommended)
    * [Running Tests](#running-tests)
    * [Updating Dependencies](#updating-dependencies)
    * [Recommended Readings](#recommended-readings)
    * [License](#license)
    * [Acknowledgements](#acknowledgements)

<!-- TOC -->

## Key Features

* **Comprehensive Plagiarism Detection**: Heimdallr scans through a vast array of sources, including web content,
  books, papers, photographs, and previous student works, leaving no room for undetected plagiarism.
* **Precise Location Identification**: It doesn't just flag potential instances of plagiarism; Heimdallr provides
  pinpoint accuracy by highlighting the exact lines or words in question, enabling users to swiftly address the issue.
* **Source Attribution**: The system not only detects plagiarism but also identifies the source that is being
  plagiarized, whether it's a website, a specific publication, or the work of another student.

## Why Heimdallr?

Heimdallr stands as a guardian of academic integrity, inspired by the mythological figure known for his unwavering
vigilance. With its advanced detection capabilities and user-friendly interface, Heimdallr is the ultimate solution
for educational institutions, researchers, and students to maintain the highest standards of academic honesty and
originality.

## Environment Variables

- Variables prefixed with `FASTAPI_` are used to configure the API UI.

| Name                         | Description                         | Default Value                      |
|------------------------------|-------------------------------------|------------------------------------|
| FASTAPI_DEBUG                | Debug Mode                          | False                              |
| FASTAPI_PROJECT_NAME         | Swagger Title                       | Heimdallr                          |
| FASTAPI_PROJECT_DESCRIPTION  | Swagger Description                 | ...                                |
| FASTAPI_PROJECT_LICENSE      | License info                        | ...                                |
| FASTAPI_PROJECT_CONTACT      | Contact details                     | ...                                |
| FASTAPI_VERSION              | Application Version                 | template.version                   |
| FASTAPI_DOCS_URL             | Swagger Endpoint                    | /docs                              |
| FASTAPI_MODEL_PATH           | Trained model path                  | /app/models/topic_predictor.joblib |
| FASTAPI_DETECT_PLAGIARISM    | Whether to detect plagiarism or not | True                               |
| FASTAPI_SIMILARITY_THRESHOLD | Minimum similarity percentage       | 0.95                               |

- Variables prefixed with `UVICORN_` are used to configure the server.

| Name              | Description           | Default Value |
|-------------------|-----------------------|---------------|
| UVICORN_HOST      | Server Host           | '127.0.0.1'   |
| UVICORN_PORT      | Server Port           | 8000          |
| UVICORN_LOG_LEVEL | Log Level             | 'info'        |
| UVICORN_RELOAD    | Enable/Disable Reload | False         |

- Variables prefixed with `MONGO_` are used for MongoDB connection.

| Name           | Description            | Default Value               |
|----------------|------------------------|-----------------------------|
| MONGO_CLIENT   | Server Host            | 'mongodb://localhost:27017' |
| MONGO_DATABASE | Server Database        | 'heimdallr-local'           |
| MONGO_USER     | User LogIn credentials | None                        |
| MONGO_PASSWORD | User credentials       | None                        |

## Continuous Integration

This project uses `make` as an adaptation layer.

Run `make help` to see all available commands.

## Quick set up

**HIGHLY RECOMMENDED**: Use `docker-compose` to run the application locally.

1. Run:

    ```bash
    docker-compose up
    ```
   This will:
    - Build the application image
    - Start a `MongoDB` server
    - Start the application
    - Train a model for topic prediction
    - Run DB migrations
2. Go to http://localhost:8000/docs to see the API documentation.
3. Use the `Verify Assignment` `POST` method to verify a document.
   You can use the [rifkin_test](rifkin_test.pdf) document as an example.
4. See the logs for the `heimdallr` service to see the results.
   e.g:
    ```log
   INFO:     Started server process [1]
   INFO:     Waiting for application startup.
   INFO:     Loading model from /app/models/topic_predictor_dev.joblib
   INFO:     Application startup complete.![img.png](img.png)
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     172.20.0.1:52912 - "POST /api/v1/assignments HTTP/1.1" 202 Accepted
   INFO:     Read Assignment(id=32750af8-bdfe-4508-a37a-5aa9718a1188, author=Franco Zanette)
   INFO:     Similar(0.992015) to Assignment(id=891bdd47-5ec0-40cf-ad42-9e7c99a78648, author=David Choren)
   INFO:     Similar(0.994410) to Assignment(id=4bdd4797-1617-45be-8b64-bd36b97908ff, author=Levy Nazareno Isaac)
   INFO:     Similar(0.991231) to Assignment(id=35cc1575-ea46-416c-95cd-260cb7efda75, author=Leon Peralta)
   ```

   > NOTE: The `POST` method returns a `202 Accepted` response. This means that the document is being verified in the
   > background

5. When verification is complete you should a log similar to:
    ```log
   INFO:     Finished comparison with Assignment(id=4bdd4797-1617-45be-8b64-bd36b97908ff, author=Levy Nazareno Isaac) in 117.274768 seconds.
   INFO:     Finished comparison with Assignment(id=35cc1575-ea46-416c-95cd-260cb7efda75, author=Leon Peralta) in 107.669727 seconds.
   INFO:     Finished comparison with Assignment(id=891bdd47-5ec0-40cf-ad42-9e7c99a78648, author=David Choren) in 147.236305 seconds.
   INFO:    Assignment e68d59ff-d725-4dfc-940a-b5ab449cf98c verified.
    ```
   > NOTE: Verification time depends on the size of the document and the number of documents in the database. It may
   mate take a while.

6. Retrieve the assignment with the `GET` method, with its `UUID` as parameter. e.g:

    ```json
   {
    "data": {
    "id": "32750af8-bdfe-4508-a37a-5aa9718a1188",
    "title": "TP5-Franco Zanette.docx.docx",
    "topic": "Emerging Systems",
    "author": "Franco Zanette",
    "similarities": [
    {
    "id": "4bdd4797-1617-45be-8b64-bd36b97908ff",
    "author": "Levy Nazareno Isaac",
    "plagiarism": 0.19135095761849497,
    "similarities": [
    {
    "present": "Puede describir el vínculo entre las leyes de la termodinámica de Newton y la “factura entrópica”.",
    "compared": "Puede describir el vínculo entre las leyes de la termodinámica de Newton y la “factura entrópica”.",
    "plagiarism": 1
    },
    {
    "present": "Qué dice Rifkin que la “internet de las cosas IOT” le aportará a la 3ra revolución industrial?",
    "compared": "Qué dice Rifkin que la “internet de las cosas IOT” le aportará a la 3ra revolución industrial?",
    "plagiarism": 1
    },
    {
    "present": "NOTA: las respuestas no deberán superar en su conjunto a 2 páginas del mismo formato que esta guía.",
    "compared": "NOTA: las respuestas no deberán superar en su conjunto a 2 páginas del mismo formato que esta guía.",
    "plagiarism": 1
    },
    {
    "present": "Podría caracterizar la Primera y Segunda revolución industrial al decir de Rifkin?",
    "compared": "Podría caracterizar la Primera y Segunda revolución industrial al decir de Rifkin?",
    "plagiarism": 1
    },
    {
    "present": "Qué inventos son las metáforas de cada infraestructura en cada una de esas etapas.",
    "compared": "Qué inventos son las metáforas de cada infraestructura en cada una de esas etapas.",
    "plagiarism": 1
    },
    {
    "present": "Qué ejemplos actuales de “procomunes” se le ocurren?",
    "compared": "Qué ejemplos actuales de “procomunes” se le ocurren?",
    "plagiarism": 1
    },
    {
    "present": "Qué límites le ve Ud. a los procomunes como forma de producción?",
    "compared": "Qué límites le ve Ud. a los procomunes como forma de producción?",
    "plagiarism": 1
    },
    {
    "present": "qué estaría faltando?",
    "compared": "qué estaría faltando?",
    "plagiarism": 1
    },
    {
    "present": "La principal limitación de los procomunes como forma de producción la incapacidad de la sociedad de proteger los recursos procomunes de la sobreexplotación por parte un individuo",
    "compared": "El internet de las cosas permitirá unificar la comunicación, la energía y la logística posibilitando la optimización de los procesos .",
    "plagiarism": 0.9502497961617389
    },
    {
    "present": "E. intangible o “sin peso”",
    "compared": "E. intangible o “sin peso”",
    "plagiarism": 1
    }
    ]
    },
    {
    "id": "35cc1575-ea46-416c-95cd-260cb7efda75",
    "author": "Leon Peralta",
    "plagiarism": 0.11538461538461539,
    "similarities": [
    {
    "present": "Qué dice Rifkin que la “internet de las cosas IOT” le aportará a la 3ra revolución industrial?",
    "compared": "Qué dice Rifkin que la “internet de las cosas IOT” le aportará a la 3ra revolución industrial?",
    "plagiarism": 1
    },
    {
    "present": "Podría caracterizar la Primera y Segunda revolución industrial al decir de Rifkin?",
    "compared": "Podría caracterizar la Primera y Segunda revolución industrial al decir de Rifkin?",
    "plagiarism": 1
    },
    {
    "present": "Qué inventos son las metáforas de cada infraestructura en cada una de esas etapas.",
    "compared": "Qué inventos son las metáforas de cada infraestructura en cada una de esas etapas.",
    "plagiarism": 1
    },
    {
    "present": "Qué límites le ve Ud. a los procomunes como forma de producción?",
    "compared": "Qué límites le ve Ud. a los procomunes como forma de producción?",
    "plagiarism": 1
    },
    {
    "present": "Qué ejemplos actuales de “procomunes” se le ocurren?",
    "compared": "Qué ejemplos actuales de “procomunes” se le ocurren?",
    "plagiarism": 1
    },
    {
    "present": "qué estaría faltando?",
    "compared": "qué estaría faltando?",
    "plagiarism": 1
    }
    ]
    },
    {
    "id": "891bdd47-5ec0-40cf-ad42-9e7c99a78648",
    "author": "David Choren",
    "plagiarism": 0.1519146892150015,
    "similarities": [
    {
    "present": "Las plataformas tecnológicas de la primera y segunda revolución industrial estaban centralizadas y sometidas a un control jerarquizado y su explotación estaba basada en la idea de que los recursos de la Tierra están para el servicio de la personas y el lucro..",
    "compared": "Las plataformas tecnológicas de la primera  y la segunda revoluciones industriales estaban centralizadas y sometidas a un control jerarquizado.",
    "plagiarism": 0.9535765262616537
    },
    {
    "present": "3.¿Qué dice Rifkin que la “internet de las cosas IOT” le aportará a la 3ra revolución industrial?",
    "compared": "Qué dice Rifkin que la “internet de las cosas IOT” le aportará a la 3ra revolución industrial?",
    "plagiarism": 0.992672017325718
    },
    {
    "present": "Qué límites le ve Ud. a los procomunes como forma de producción?",
    "compared": "Qué límites le ve Ud. a los procomunes como forma de producción?",
    "plagiarism": 1
    },
    {
    "present": "NOTA: ​las respuestas no deberán superar en su conjunto a 2 páginas del mismo formato que esta guía.",
    "compared": "NOTA: las respuestas no deberán superar en su conjunto a 2 páginas del mismo formato que esta guía.",
    "plagiarism": 0.9813714487124504
    },
    {
    "present": "qué estaría faltando?",
    "compared": "qué estaría faltando?",
    "plagiarism": 1
    },
    {
    "present": "2.¿Podría caracterizar la Primera y Segunda revolución industrial al decir de Rifkin?",
    "compared": "Podría caracterizar la Primera y Segunda revolución industrial al decir de Rifkin?",
    "plagiarism": 0.989975333730042
    },
    {
    "present": "E. intangible o “sin peso”",
    "compared": "E. intangible o “sin peso”",
    "plagiarism": 1
    },
    {
    "present": "5.¿Qué ejemplos actuales de “procomunes” se le ocurren?",
    "compared": "Qué ejemplos actuales de “procomunes” se le ocurren?",
    "plagiarism": 0.9819685131502129
    }
    ]
    }
    ]
    }
    }
    ```

7. To stop the application run:

    ```bash
    docker-compose down
    ```

## Development Environment

### Installing Poetry

This package uses poetry for dependency management and `Python 3.10` as interpreter.

Install poetry in the system `site_packages`. DO NOT INSTALL IT in a virtual environment itself.

To install poetry, run:

```bash
pip install poetry
```

### Building the Development Environment

1. Clone the repository

    ```bash
    git clone "git@github.com:tomasanchez/heimdallr.git"
    ```
2. Install dependencies

    ```bash
    cd cosmic-fastapi && poetry install
    ```

   Note that poetry doesn't activate the virtual environment for you. You have to do it manually.
   Or prefix subsequent the commands with

    ```bash
    poetry run
    ```

   You can view the environment that poetry uses with

    ```bash
    poetry env info
    ```

   To activate run:

    ```bash
    poetry shell
    ```
3. Download `spaCy` trained Spanish Model

    ```bash
    poetry run python -m spacy download es_core_news_lg
    ```
4. Train model for topic prediction (Optional)
    - Run script
   ```bash
    poetry run python -m heimdallr.train
   ```
    - Update `FASTAPI_MODEL_PATH` environment variable with the new model path
        ```bash
        export FASTAPI_MODEL_PATH=/path/to/new/model
        ```


5. Activate pre-commit hooks (Optional)

   Using [pre-commit](https://pre-commit.com/) to run some checks before committing is highly recommended.

   To activate the pre-commit hooks run:

    ```bash
    pre-commit install
    ```

   To run the checks manually run:

    ```bash
    poetry run pre-commit run --all-files
    ```

   The following checks are run: `black`, `flake8`, `isort`, `mypy`, `pylint`.

## Running Local

1. Either:

    ```bash
    poetry run python -m heimdallr.main
    ```

   > NOTE: A`MongoDB` server running to verify documents. `docker-compose.yml` contains a service configured for that.

2. Go to http://localhost:8000/docs to see the API documentation.

### MSWord Document Support

For supporting `.doc` files you **must** have `antiword` installed. Otherwise, the API will not verify `.doc` files, but
It will still work for `.pdf` and

If using `Ubuntu`, run:

```bash
sudo apt-get update -y && sudo apt-get install -y antiword
```

If using `Mac OSX`, run:

```bash
brew install antiword
```

### Using Docker (Recommended)

Run the application in docker. Requires no further configuration.

1. Run:
    ```bash
    docker-compose up
    ```
2. Go to http://localhost:8000/docs to see the API documentation.

## Running Tests

You can run the tests with:

```bash
poetry run pytest
```

or with the `make` command:

```bash
make test
```

To generate a coverage report add `--cov src`.

```bash
poetry run pytest --cov src
```

Or with the `make` command:

```bash
make cover
```

## Updating Dependencies

To update the dependencies run:

```bash
poetry update
```

## What's missing?

- **Performance improvements**:
    - Maybe filter documents by topic. Right now, all documents are being compared.
    - There is a lot to improve about processing speed. A possible solution is to use a `Celery` task queue to process
      documents in the background, as using `spaCy` is CPU intensive.
    - Better response management. Right now, if a document is being processed, the API will return a `202 Accepted`
      response, but it is impossible to know any errors that may occur during processing. It's only possible to know
      when the process is finished by checking the logs. Or if by retrieving its ID it doesn't return a `404 Not Found`.
- **Interesting Topics**: their definition was more related to what were the assignment requirements.
- **Internet scrapping**: It was not implemented due to time constraints. It would be a great addition to the system.
  Also, it would relative easy to implement: an `Adapter` capable of scrapping the web and returning an `Assignment`
  will do the job.
- **Batch Processing**
- **Title Identification**: Only file names are used to identify documents. More NLP domain knowledge is needed to
  identify titles.
- **Better Author recognition**: Right now is using the first *identified* name. Some documents don't include authors
  name, others aren't their name first mentioned. Sometimes another token is wrongly recognized as a `PER` token.
- **Requirements Identification**: Requirements are being considered as plagiarism. A better approach would be to
  identify them and exclude them from the comparison like for each topic have a list of requirements and exclude them.

## Recommended Readings

- [FastAPI official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic official Documentation](https://pydantic-docs.helpmanual.io/)
- [Cosmic Python](https://cosmicpython.com/)
- [Cosmic FastAPI template](https://github.com/tomasanchez/cosmic-fastapi)
- [spaCy Documentation](https://spacy.io/)

## License

This project is licensed under the terms of the MIT license unless otherwise specified. See [`LICENSE`](LICENSE) for
more details or visit https://mit-license.org/.

## Acknowledgements

This project was designed and developed
by [Tomás Sánchez](https://tomsanchez.com.ar/about/) <[info@tomsanchez.com.ar](mailto:info@tomsanchez.com.ar)>.

If you find this project useful, please consider supporting its development by sponsoring it.