from dataclasses import dataclass


@dataclass
class Stage:  # pylint: disable=too-many-instance-attributes
    """
    object to represent a pytest test stage
    """

    stageid: str
    testid: str
    sessionid: str
    environment: str
    app_version: str
    stage: str
    outcome: str
    longreprtext: str
    capstdout: str
    capstderr: str
    sections: dict
    user_properties: dict
    caplog: str
    timestamp: str
