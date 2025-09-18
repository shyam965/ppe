from configs_and_constants.env import env
import jwt
from datetime import datetime, timedelta

access_token_secret = env.get("access_token_secret")
refresh_token_secret = env.get("refresh_token_secret")


def generate_access_token(payload: dict, expires_in_minutes: int = 30):
    payload.update(
        {
            "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes),
            "iat": datetime.utcnow(),
        }
    )
    return jwt.encode(payload, access_token_secret, algorithm="HS256")


def generate_refresh_token(payload: dict, expires_in_days: int = 7):
    payload.update(
        {
            "exp": datetime.utcnow() + timedelta(days=expires_in_days),
            "iat": datetime.utcnow(),
        }
    )
    return jwt.encode(payload, refresh_token_secret, algorithm="HS256")


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, access_token_secret, algorithms=["HS256"])
        return None, payload
    except Exception as error:
        return str(error), None


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, refresh_token_secret, algorithms=["HS256"])
        return None, payload
    except Exception as error:
        return str(error), None
