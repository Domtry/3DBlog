from datetime import timedelta, datetime
from typing import Any

import jwt
from cryptography.fernet import Fernet

JWT_SECRET_KEY = "DyC@d£"
JWT_ENCRYPT_KEY = b'D-F3GiOIlschrxeX7MqoqTcYDHn04w0rze9QHW97Id8='
JWT_ALGO = "HS256"


def is_valid_password(current_password: str, current_encrypt_pwd: Any, encrypt_key: Any) -> bool:
    fernet = Fernet(encrypt_key)
    password = fernet.decrypt(current_encrypt_pwd).decode(encoding = "UTF-8")
    return current_password == password


def generate_token(user_id: str | int, roles: list[str], expire_at: timedelta, is_refresh: bool = False) -> str:
    payload = {
        "algo": JWT_ALGO,
        "is_refresh": is_refresh,
        "create_at": str(datetime.now()),
        "expire_at": str(datetime.now() + expire_at),
        "user_id": user_id,
        "roles": roles
    }

    partial_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm = JWT_ALGO)
    fernet = Fernet(JWT_ENCRYPT_KEY)
    byte_token = fernet.encrypt(partial_token.encode(encoding = 'UTF-8', errors = 'strict'))
    return byte_token.decode("utf-8")


def get_token_info(access_token: str) -> dict[str, Any]:
    try:
        byte_token = access_token.encode(encoding = 'UTF-8', errors = 'strict')
        fernet = Fernet(JWT_ENCRYPT_KEY)
        partial_token = fernet.decrypt(byte_token)
        return jwt.decode(partial_token.decode("utf-8"), key = JWT_SECRET_KEY, algorithms = [JWT_ALGO])
    except Exception:
        raise Exception('Token invalid')
