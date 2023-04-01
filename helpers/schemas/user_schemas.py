import re

from marshmallow import Schema, fields, ValidationError


def hard_password(password: str):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    if re.match(pattern, password) is None:
        raise ValidationError('Password has incorrect format.')


class UserRegisterSchema(Schema):
    username = fields.Str(required=True, nullable=False)
    password = fields.Str(required=True, nullable=False, validate=hard_password)


class UserPutSchemasSchema(Schema):
    username = fields.Str(required=True, nullable=False)


class UserChangePasswordSchema(Schema):
    old_password = fields.Str(required=True, nullable=False)
    new_password = fields.Str(required=True, nullable=False, validate=hard_password)

