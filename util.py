from datetime import datetime
from datetime import timezone


def timestamp():
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
