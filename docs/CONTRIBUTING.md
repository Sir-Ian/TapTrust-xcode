# Contributing

Thank you for helping out! This project uses [Poetry](https://python-poetry.org/) for dependency management and has a simple CI pipeline.

## Setup

1. Install Poetry if you don't have it:

   ```bash
   pip install poetry
   ```

2. Install all dependencies (including development tools):

   ```bash
   poetry install --with dev
   ```

## Code Style

We run `flake8` on the `verifier/` package. Please lint before pushing:

```bash
poetry run flake8 verifier
```

## Running Tests

Run the full test suite with:

```bash
poetry run pytest
```

## Branches and Pull Requests

* Use feature branches named after the work you are doing, e.g. `feature/nfc-support`.
* Keep commits focused and descriptive.
* Open a pull request against `main` when the feature is ready and all tests pass.
* CI will run flake8 and pytest on your PR.
