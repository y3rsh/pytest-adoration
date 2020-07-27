import uuid
import os
import logging
import pytest
import db
from zippopotam_client import ZippopotamClient
from session import Session
import util

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="api.zippopotam.us")


@pytest.fixture
def zippopotam_client(request) -> ZippopotamClient:
    return ZippopotamClient(request.config.getoption("--base-url"))


@pytest.fixture(autouse=True)
def test_run_id(request, record_property):
    """
        Runs before each test.
        testexecutionid will be the same for each test run in this collection
    """
    pass
    # record_property("testexecutionid", str(uuid.uuid4().hex))


# after we know what tests are collected to run
def pytest_report_collectionfinish(config, startdir, items):
    sessionid = str(uuid.uuid4().hex)  # generate a unique id for the test session
    logger.info(f"sessionid is {sessionid}")
    pytest.session = Session(
        sessionid,
        os.environ.get("ENVIRONMENT", "empty"),
        os.environ.get("APP_VERSION", "empty"),
        util.timestamp(),
        [item.nodeid for item in items],
    )
    logger.info(pytest.session.collected_tests)
    db.put_session(pytest.session)


# after each test stage
def pytest_runtest_logreport(report):
    pytest.session.add_stage(
        report.nodeid, report.when, report.outcome, util.timestamp()
    )
    db.put_session(pytest.session)


# after all tests finished
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    pytest.session.finish_time = util.timestamp()
    # todo add test result data to the object
    print(vars(terminalreporter))
    logger.info(pytest.session.stages)
    db.put_session(pytest.session)
