from dataclasses import dataclass


@dataclass
class Stage:
    stageid: str
    testid: str
    sessionid: str
    environment: str
    app_version: str
    stage: str
    outcome: str
    timestamp: str
