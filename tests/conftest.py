import pytest
from zippopotam_client import ZippopotamClient


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="api.zippopotam.us")


@pytest.fixture
def zippopotam_client(request) -> ZippopotamClient:
    return ZippopotamClient(request.config.getoption("--base-url"))
