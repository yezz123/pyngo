set shell := ["bash", "-uc"]

ENV := env('ENV', '')

_default:
    @just --list


clean:
    rm -f `find . -type f -name '*.py[co]' `
    rm -f `find . -type f -name '*~' `
    rm -f `find . -type f -name '.*~' `
    rm -f `find . -type f -name .coverage`
    rm -f `find . -type f -name ".coverage.*"`
    rm -rf `find . -name __pycache__`
    rm -rf `find . -type d -name '*.egg-info' `
    rm -rf `find . -type d -name 'pip-wheel-metadata' `
    rm -rf `find . -type d -name .pytest_cache`
    rm -rf `find . -type d -name .ruff_cache`
    rm -rf `find . -type d -name .cache`
    rm -rf `find . -type d -name .mypy_cache`
    rm -rf `find . -type d -name htmlcov`
    rm -rf `find . -type d -name "*.egg-info"`
    rm -rf `find . -type d -name build`
    rm -rf `find . -type d -name dist`


format:
    uv run pre-commit run --all-files --verbose --show-diff-on-failure


lint:
    uv run mypy --show-error-codes pyngo


test:
    @echo "ENV={{ENV}}"
    export PYTHONPATH=.
    uv run pytest --cov=pyngo --cov=tests --cov-report=term-missing --cov-fail-under=80


test-html:
    @echo "ENV={{ENV}}"
    export PYTHONPATH=.
    uv run pytest --cov=pyngo --cov=tests --cov-report=html
