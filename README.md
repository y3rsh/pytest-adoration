# Pytest Adoration

> pytest is my favorite test framework.

## Prerequisites

- Locally install python 3.8.4 and poetry and have on your path.
- run the commands in the project directory

### Notes

- using pytest 6, `poetry add pytest --allow-prerelease`
- poetry gives us the functionality of update and manages our virtual environment
- poetry gives us a deterministic requirements.txt with hashes
- in out containers we want to use only pip as it is fast at downloading and installing dependencies
- See virtual env being used by poetry `poetry show -v`
- build or use built in test strategies to generate test data, hypothesis https://github.com/HypothesisWorks/hypothesis
- pytest.ini - configuration for pytest
- test/conftest.py - a place for global fixtures and custom configuration of built in features of pytest
- invoke is a tool like make
- `poetry run invoke ready` lint with black and flake8 and make sure the requirements.txt is up to date
- run tests `poetry run pytest --log-cli-level debug`

## todo

- add pre and post test methods to live update status by posting to dynamo?
- get a container with this running in AWS
- example to show the live test data - grab from dynamo and display
- xfail
- different paramaterization methods
- test generation
- hypothesis example
- always failing test?
- mocking, monkeypatch unit examples?
