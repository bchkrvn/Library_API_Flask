from marshmallow import Schema, fields

from app.helpers.schemas.tools import not_empty_string


class NewsValidateSchema(Schema):
    text = fields.Str(required=True, nullable=False, validate=not_empty_string)
