import base64
import hashlib
import hmac

from flask import current_app


def create_hash(password):
    hash_password = hashlib.pbkdf2_hmac(
        current_app.config["HASH_NAME"],
        password.encode('utf-8'),
        current_app.config["PWD_HASH_SALT"],
        current_app.config["PWD_HASH_ITERATIONS"]
    )
    return hash_password


def get_hash(password):
    return base64.b64encode(create_hash(password))


def compare_password(right_password, other_password) -> bool:
    decode_right_password = base64.b64decode(right_password)
    hash_other_password = create_hash(other_password)
    return hmac.compare_digest(decode_right_password, hash_other_password)
