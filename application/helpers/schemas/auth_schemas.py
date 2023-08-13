from marshmallow import Schema, fields
from .validators import not_empty_string


class AuthPostSchema(Schema):
    username = fields.Str(required=True, nullable=False, validate=not_empty_string)
    password = fields.Str(required=True, nullable=False, validate=not_empty_string)


class AuthPutSchema(Schema):
    refresh_token = fields.Str(required=True, nullable=False)
