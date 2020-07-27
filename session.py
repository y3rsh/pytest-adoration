from typing import List
from dataclasses import dataclass
from dataclasses import field


@dataclass
class Session:
    sessionid: str
    environment: str
    app_version: str
    start_time: str
    collected_tests: List[str]
    stages: List[dict] = field(default_factory=lambda: [])
    finish_time: str = None

    def add_stage(self, testid, stage, outcome, timestamp):
        self.stages.append(
            {
                "testid": testid,
                "stage": stage,
                "outcome": outcome,
                "timestamp": timestamp,
            }
        )
