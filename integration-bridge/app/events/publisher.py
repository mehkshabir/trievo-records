import json
from datetime import datetime, timezone
from app.core import config

EVENT_LOG: list = []
_r = None
if config.REDIS_URL:
    import redis
    _r = redis.from_url(config.REDIS_URL)

def publish(event: str, payload: dict):
    """Redis Streams when configured (CRM + Dashboard consume), else in-memory log."""
    body = {"event": event, "at": datetime.now(timezone.utc).isoformat(), **payload}
    EVENT_LOG.append(body)
    if _r: _r.xadd(event, {"data": json.dumps(body)})
