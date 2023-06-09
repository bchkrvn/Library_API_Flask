from marshmallow import Schema, fields

from helpers.schemas.tools import not_empty_string


class CommentsSchema(Schema):
    text = fields.Str(required=True, nullable=False, validate=not_empty_string)
