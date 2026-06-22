import redis
from config import REDIS_URL

# Connexion partagée par tout le projet
client = redis.from_url(REDIS_URL, decode_responses=True)

def ping():
    try:
        return client.ping()
    except Exception:
        return False
