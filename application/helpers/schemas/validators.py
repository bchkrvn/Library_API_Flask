import re

from marshmallow import ValidationError


def not_empty_string(string):
    if string == '':
        raise ValidationError('field cannot be an empty string.')


def hard_password(password: str):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    if re.match(pattern, password) is None:
        raise ValidationError('Password has incorrect format.')
