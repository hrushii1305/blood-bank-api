import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

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