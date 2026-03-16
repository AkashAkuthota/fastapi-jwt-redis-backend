import logging
from fastapi import HTTPException, status, Request
from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)

Login_attempts = 5
Login_window = 60


def check_login_rate_limits(ip: str, email: str):

    IP_key = f"login:ip:{ip}"
    Email_key = f"login:email:{email}"

    IP_attempts = redis_client.incr(IP_key)
    Email_attempts = redis_client.incr(Email_key)

    if IP_attempts == 1:
        redis_client.expire(IP_key, Login_window)

    if Email_attempts == 1:
        redis_client.expire(Email_key, Login_window)

    logger.info(
    f"event=login_attempt ip={ip} email={email} ip_attempts={IP_attempts} email_attempts={Email_attempts}"
    )   

    if IP_attempts > Login_attempts or Email_attempts > Login_attempts:

        logger.warning(
        f"event=login_rate_limit_exceeded ip={ip} email={email}"
        )

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again in 60 seconds."
        )


refresh_IP_limts = 10
refresh_user_limts = 5
refresh_window = 60


def check_refresh_rate_limit(ip: str, user_id: int):

    IP_key = f"refresh:ip:{ip}"
    user_key = f"refresh:user_id:{user_id}"

    IP_attempts = redis_client.incr(IP_key)
    user_attempts = redis_client.incr(user_key)

    if IP_attempts == 1:
        redis_client.expire(IP_key, refresh_window)

    if user_attempts == 1:
        redis_client.expire(user_key, refresh_window)

    logger.info(
    f"event=refresh_attempt ip={ip} user_id={user_id} ip_attempts={IP_attempts} user_attempts={user_attempts}"
    )

    if IP_attempts > refresh_IP_limts:

        logger.warning(
            f"event=refresh_rate_limit_exceeded ip={ip} user_id={user_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many refresh attempts from this IP."
        )

    if user_attempts > refresh_user_limts:

        logger.warning(
            f"event=refresh_rate_limit_exceeded ip={ip} user_id={user_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many refresh attempts from this user."
        )

async def login_rate_limiter(request: Request):

    try:
        body = await request.json()
        email = body.get("email", "unknown").lower()
    except Exception:
        email = "unknown"

    client_ip = request.headers.get("x-forwarded-for")

    if client_ip:
        client_ip = client_ip.split(",")[0]
    else:
        client_ip = request.client.host

    check_login_rate_limits(client_ip, email)



