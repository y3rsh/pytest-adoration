from typing import List
from dataclasses import dataclass


@dataclass
class Session:
    sessionid: str
    environment: str
    app_version: str
    start_time: str
    collected_tests: List[str]
    finish_time: str = None
