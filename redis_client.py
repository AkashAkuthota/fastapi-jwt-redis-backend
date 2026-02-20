import redis
import os
import hashlib
from datetime import datetime, timezone
from dotenv import load_dotenv


load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT  = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

redis_pool = redis.ConnectionPool(
    host = REDIS_HOST,
    port = REDIS_PORT,
    db = REDIS_DB,
    decode_responses = True
)

redis_client = redis.Redis(connection_pool=redis_pool)

def hashing_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()


def blacklist_token(token : str, expires_at : datetime):
    hashed = hashing_token(token)

    now = datetime.now(timezone.utc)

    ttl_seconds = int((expires_at - now).total_seconds())

    if ttl_seconds > 0:
        redis_client.setex(f"blacklist:{hashed}", ttl_seconds, "revoked")

def is_token_blacklisted(token : str) -> bool:
    hashed = hashing_token(token)
    return redis_client.exists(f"blacklist:{hashed}")
