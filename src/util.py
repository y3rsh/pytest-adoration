from datetime import datetime
from datetime import timezone


def timestamp():
    """
    timestamp to use in the project
    """
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
