import uuid
import os
import logging
import pytest
import src.db.dynamo as db
from src.zippopotam.zippopotam_client import ZippopotamClient
from src.db.session import Session
from src.db.stage import Stage
import src.util as util

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="api.zippopotam.us")
    parser.addoption(
        "--remote-dynamo",
        action="store_true",
        default=False,
    )


@pytest.fixture
def zippopotam_client(request) -> ZippopotamClient:
    return ZippopotamClient(request.config.getoption("--base-url"))


def pytest_runtest_logstart(nodeid, location):
    """
    Runs before each test.
    """
    pytest.testid = str(uuid.uuid4().hex)


# after we know what tests are collected to run
def pytest_report_collectionfinish(config, startdir, items):
    if config.getoption("--remote-dynamo"):
        logger.info("Using remote dynamo")
        pytest.db = db.Dynamo(False)
    else:
        logger.info("Using local dynamo")
        pytest.db = db.Dynamo()
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
    pytest.db.put_session(pytest.session)


# after each test stage
def pytest_runtest_logreport(report):
    stageid = pytest.testid + "-" + report.when  # unique id
    logger.info(f"stageid = {stageid}")
    stage = Stage(
        stageid,
        report.nodeid,
        pytest.session.sessionid,
        pytest.session.environment,
        pytest.session.app_version,
        report.when,
        report.outcome,
        util.timestamp(),
    )
    logger.debug("stage is: {stage}")
    pytest.db.put_stage(stage)


# after all tests finished
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    pytest.session.finish_time = util.timestamp()
    # todo add test result data to the session
    pytest.db.put_session(pytest.session)
