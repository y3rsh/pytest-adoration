from typing import List
from dataclasses import dataclass


@dataclass
class Session:
    """
    object to represent a session of tests
    this is all tests collected by a command argument to pytest
    """

    sessionid: str
    environment: str
    app_version: str
    start_time: str
    collected_tests: List[str]
    finish_time: str = None
