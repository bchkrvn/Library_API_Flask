from marshmallow import Schema, fields

from .validators import not_empty_string


class CommentsSchema(Schema):
    text = fields.Str(required=True, nullable=False, validate=not_empty_string)
