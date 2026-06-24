import redis
from config import REDIS_URL

client = redis.from_url(REDIS_URL, decode_responses=True)


def ping():
    try:
        return client.ping()
    except Exception:
        return False
