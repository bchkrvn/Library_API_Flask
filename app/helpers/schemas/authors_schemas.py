from marshmallow import Schema, fields

from .tools import not_empty_string


class AuthorSchema(Schema):
    first_name = fields.Str(required=True, nullable=False, validate=not_empty_string)
    last_name = fields.Str(required=True, nullable=False, validate=not_empty_string)
    middle_name = fields.Str(required=True, nullable=False, validate=not_empty_string)


class AuthorPutSchema(Schema):
    first_name = fields.Str(required=False, nullable=False, validate=not_empty_string)
    last_name = fields.Str(required=False, nullable=False, validate=not_empty_string)
    middle_name = fields.Str(required=False, nullable=False, validate=not_empty_string)
