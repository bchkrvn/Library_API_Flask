from flask import request, abort, current_app
import jwt

from constants import JWT_SECRET, JWT_ALGO
from container import user_service


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=[current_app.config["JWT_ALGO"]])
        except Exception as e:
            abort(400)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            user = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=[current_app.config["JWT_ALGO"]])
            role = user.get('role', 'user')
        except Exception as e:
            abort(400)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def user_required(func):
    def wrapper(*args, **kwargs):
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            user_data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
            user = user_service.get_by_username(user_data['username'])
        except Exception as e:
            abort(400)

        return func(*args, **kwargs, u_id=user.id)

    return wrapper
