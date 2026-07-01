import redis
import json
import os

# Connect to Redis (Railway provides REDIS_URL)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_cache(key: str):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception:
        return None

def set_cache(key: str, value: dict, expire_seconds: int = 60):
    try:
        redis_client.setex(key, expire_seconds, json.dumps(value))
    except Exception:
        pass