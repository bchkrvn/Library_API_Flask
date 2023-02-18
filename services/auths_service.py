import calendar
import datetime

from constants import JWT_SECRET, JWT_ALGO
from services.users_service import UserService
from flask import abort
import jwt


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh=True):
        user = self.user_service.get_by_username(username)
        if not user:
            abort(400)

        if not is_refresh:
            is_right_password = self.user_service.compare_password(user.password, password)
            print(2)
            if not is_right_password:
                abort(400)
        data = {
            'username': user.username,
            'role': user.role,
        }
        min10 = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        data['exp'] = calendar.timegm(min10.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return tokens

    def approve_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGO])
            username = data.get('username')
        except Exception as e:
            abort(400)

        return self.generate_token(username, None, is_refresh=True)

