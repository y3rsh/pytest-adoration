# Pytest Adoration

> pytest is my favorite test framework.

## Prerequisites

- Locally install python 3.8.4 and poetry and have on your path.
- run the commands in the project directory
- docker if you want the local DB

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
- add action to generate the requirements.txt on push

## Important environment variables

Most CI systems make it easy to set environment variables so we will use them to inform our reporting what is under test.

### ENVIRONMENT

> What environment is the test running against - set to `empty` if not defined

### APP_VERSION

> What version of the app the test is running against - set to `empty` if not defined

### DYNAMO_LOCAL_URL

> "http://localhost:8000" is hard coded but can be overridden

## Local execution (relative commands in project root dir)

1. start the local dynamo
    - `docker-compose up`
2. make sure everything is installed
    - `poetry install`
3. create the table locally
    - `poetry run python dynamo.py`
4. run the tests using local dynamo
    - `poetry run pytest --log-cli-level debug`
5. run the tests using remote dynamo (AWS CLI config read by boto)
    - `poetry run pytest --remote-dynamo --log-cli-level debug`