from marshmallow import Schema, fields

from helpers.schemas.tools import hard_password, not_empty_string


class UserRegisterSchema(Schema):
    username = fields.Str(required=True, nullable=False, validate=not_empty_string)
    password = fields.Str(required=True, nullable=False, validate=hard_password)


class UserPutSchemasSchema(Schema):
    username = fields.Str(required=True, nullable=False, validate=not_empty_string)


class UserChangePasswordSchema(Schema):
    old_password = fields.Str(required=True, nullable=False, validate=not_empty_string)
    new_password = fields.Str(required=True, nullable=False, validate=hard_password)
