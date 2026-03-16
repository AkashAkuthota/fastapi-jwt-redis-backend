from fastapi import HTTPException, status
from app.core.redis_client import redis_client

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

    if IP_attempts > Login_attempts or Email_attempts > Login_attempts:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts, please try again")
    

refresh_IP_limts = 10
refresh_user_limts = 5
refresh_window = 60

def check_refresh_rate_limit(ip : str, user_id : int):

    IP_key = f"refresh:ip:{ip}"
    user_key = f"refresh:user_id:{user_id}"

    IP_attempts = redis_client.incr(IP_key)
    user_attempts = redis_client.incr(user_key)

    if IP_attempts == 1:
        redis_client.expire(IP_key, refresh_window)
    
    if user_attempts == 1:
        redis_client.expire(user_key, refresh_window)


    if IP_attempts > refresh_IP_limts:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Too many refresh attempts from this IP")
    
    if user_attempts > refresh_user_limts:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Too many refresh attempts from this user")
    