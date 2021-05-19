import time
from datetime import datetime
from datetime import timezone


def timestamp():
    """
    timestamp to use in the project
    """
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()


def timestamp_milliseconds() -> int:
    """
    timestamp as integer milliseconds from epoch
    """
    return int(round(time.time() * 1000))
