import functools

import jwt
from flask import request, abort, current_app

from container import user_service


def auth_required(func):
    """
    Проверка авторизован ли пользователь
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401, "Headers don't have token")
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=[current_app.config["JWT_ALGO"]])
        except Exception as e:
            abort(401, 'You are not authorized')

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    Проверка - является ли пользователь администратором
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            user = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=[current_app.config["JWT_ALGO"]])
            role = user.get('role', 'user')
        except Exception as e:
            abort(401, 'You are not authorized')

        if role != 'admin':
            abort(403, 'You are not admin')

        return func(*args, **kwargs)

    return wrapper


def user_required(func):
    """
    Проверка - кем является пользователь
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401, "You didn't send token")

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            user_data = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=[current_app.config["JWT_ALGO"]])
            user = user_service.get_by_username(user_data['username'])
        except Exception as e:
            abort(401, 'You are not authorized')

        return func(*args, **kwargs, u_id=user.id)

    return wrapper
