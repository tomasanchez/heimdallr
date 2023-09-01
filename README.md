# Heimdallr

A powerful and intelligent plagiarism detection system designed to uphold academic integrity and ensure the authenticity
of written works. Named after Heimdallr, the all-seeing Norse god, this system possesses unparalleled vigilance and a
watchful eye over the realm of academic content.

## Content

<!-- TOC -->

* [Heimdallr](#heimdallr)
    * [Content](#content)
    * [Key Features](#key-features)
    * [Environment Variables](#environment-variables)
    * [Continuous Integration](#continuous-integration)
    * [Development Environment](#development-environment)
        * [Installing Poetry](#installing-poetry)
        * [Building the Development Environment](#building-the-development-environment)
    * [Running Local](#running-local)
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

Variables prefixed with `FASTAPI_` are used to configure the API UI.

| Name                        | Description         | Default Value    |
|-----------------------------|---------------------|------------------|
| FASTAPI_DEBUG               | Debug Mode          | False            |
| FASTAPI_PROJECT_NAME        | Swagger Title       | API GATEWAY      |
| FASTAPI_PROJECT_DESCRIPTION | Swagger Description | ...              |
| FASTAPI_PROJECT_LICENSE     | License info        | ...              |
| FASTAPI_PROJECT_CONTACT     | Contact details     | ...              |
| FASTAPI_VERSION             | Application Version | template.version |
| FASTAPI_DOCS_URL            | Swagger Endpoint    | /docs            |

Variables prefixed with `UVICORN_` are used to configure the server.

| Name              | Description           | Default Value |
|-------------------|-----------------------|---------------|
| UVICORN_HOST      | Server Host           | '127.0.0.1'   |
| UVICORN_PORT      | Server Port           | 8000          |
| UVICORN_LOG_LEVEL | Log Level             | 'info'        |
| UVICORN_RELOAD    | Enable/Disable Reload | False         |

## Continuous Integration

This project uses `make` as an adaptation layer.

Run `make help` to see all available commands.

## Development Environment

### Installing Poetry

This package uses poetry for dependency management.

Install poetry in the system `site_packages`. DO NOT INSTALL IT in a virtual environment itself.

To install poetry, run:

```bash
pip install poetry
```

### Building the Development Environment

1. Clone the repository

    ```bash
    git clone "git@github.com/tomasanchez/cosmic-fastapi.git"
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
3. Activate pre-commit hooks (Optional)

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

1. Run:

    ```bash
    poetry run python -m heimdallr.main
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

## Recommended Readings

- [FastAPI official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic official Documentation](https://pydantic-docs.helpmanual.io/)
- [Cosmic Python](https://cosmicpython.com/)

## License

This project is licensed under the terms of the MIT license unless otherwise specified. See [`LICENSE`](LICENSE) for
more details or visit https://mit-license.org/.

## Acknowledgements

This project was designed and developed
by [Tomás Sánchez](https://tomsanchez.com.ar/about/) <[info@tomsanchez.com.ar](mailto:info@tomsanchez.com.ar)>.

If you find this project useful, please consider supporting its development by sponsoring it.