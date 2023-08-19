import base64
import hashlib
import hmac

from flask import current_app


def _create_hash(password: str) -> bytes:
    """make hash from password"""
    hash_password = hashlib.pbkdf2_hmac(
        current_app.config["HASH_NAME"],
        password.encode('utf-8'),
        current_app.config["PWD_HASH_SALT"],
        current_app.config["PWD_HASH_ITERATIONS"]
    )
    return hash_password


def get_hash(password: str) -> str:
    """get hash from password"""
    return base64.b64encode(_create_hash(password)).decode()


def compare_password(right_password: str, other_password: str) -> bool:
    """compare password's hash"""
    decode_right_password = base64.b64decode(right_password.encode())
    hash_other_password = _create_hash(other_password)
    return hmac.compare_digest(decode_right_password, hash_other_password)
