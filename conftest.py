import uuid
import os
import logging
import pytest
from pytest_html import extras
import src.db.dynamo as db
from src.zippopotam.zippopotam_client import ZippopotamClient
from src.db.session import Session
from src.db.stage import Stage
import src.util as util

logger = logging.getLogger(__name__)
# pylint: disable:unused-argument


def pytest_addoption(parser):
    """
    add CLI options
    """
    parser.addoption("--base-url", action="store", default="api.zippopotam.us")
    parser.addoption(
        "--remote-dynamo",
        action="store_true",
        default=False,
    )


@pytest.fixture
def zippopotam_client(request) -> ZippopotamClient:
    """
    API client
    """
    return ZippopotamClient(request.config.getoption("--base-url"))


def pytest_runtest_logstart():
    """
    Runs before each test.
    """
    pytest.testid = str(uuid.uuid4().hex)


def pytest_report_collectionfinish(config, items):
    """
    after we know what tests are collected to run
    """
    if config.getoption("--remote-dynamo"):
        logger.info("Using remote dynamo")
        pytest.db = db.Dynamo(False)
    else:
        logger.info("Using local dynamo")
        pytest.db = db.Dynamo()
    sessionid = str(uuid.uuid4().hex)  # generate a unique id for the test session
    logger.info(f"sessionid is {sessionid}")
    test_names_and_marks = [
        {
            "testid": item.nodeid,
            "metadata": next(
                iter(
                    [
                        arg
                        for arg in [
                            marker.kwargs
                            for marker in item.own_markers
                            if marker.name == "meta"
                        ]
                        if arg
                    ]
                ),
                [],
            )
            if "meta" in [marker.name for marker in item.own_markers]
            else [],
        }
        for item in items
    ]
    pytest.session = Session(
        sessionid,
        os.environ.get("ENVIRONMENT", "empty"),
        os.environ.get("APP_VERSION", "empty"),
        util.timestamp(),
        test_names_and_marks,
    )
    logger.info(pytest.session.collected_tests)
    pytest.db.put_session(pytest.session)


def pytest_runtest_logreport(report):
    """
    after each test stage
    """
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
        report.longreprtext,
        report.capstdout,
        report.capstderr,
        dict(report.sections),
        dict(report.user_properties),
        report.caplog,
        util.timestamp(),
    )
    logger.debug("stage is: {stage}")
    pytest.db.put_stage(stage)


def pytest_terminal_summary():
    """
    after all tests finish
    """
    pytest.session.finish_time = util.timestamp()
    pytest.db.put_session(pytest.session)


@pytest.fixture(autouse=True, scope="function")
def add_metadata_to_reports(request, record_property, extra):
    """
    add the keyword arguments from the meta mark to the html and junit reports
    """
    if not request.node.own_markers:
        logger.warning(f"test: {request.node.name} has no markers")
        return
    metadata = (
        next(
            iter(
                [
                    arg
                    for arg in [
                        marker.kwargs
                        for marker in request.node.own_markers
                        if marker.name == "meta"
                    ]
                    if arg
                ]
            ),
            [],
        )
        if "meta" in [marker.name for marker in request.node.own_markers]
        else []
    )
    for metadata_key in metadata:
        extra.append(
            extras.html(
                f"""<p>{metadata_key}: {metadata.get(metadata_key, None)}</p>"""
            )
        )
        record_property(metadata_key, metadata.get(metadata_key, None))
