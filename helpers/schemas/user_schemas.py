from marshmallow import Schema, fields

from helpers.schemas.tools import hard_password, not_empty_string


class UserSchema(Schema):
    username = fields.Str(required=True, nullable=False, validate=not_empty_string)
    password = fields.Str(required=True, nullable=False, validate=hard_password)


class UserPasswordSchema(Schema):
    old_password = fields.Str(required=True, nullable=False, validate=not_empty_string)
    new_password = fields.Str(required=True, nullable=False, validate=hard_password)
