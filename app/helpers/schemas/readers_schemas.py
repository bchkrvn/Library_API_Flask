from marshmallow import Schema, fields

from app.helpers.schemas.tools import not_empty_string


class ReaderSchema(Schema):
    first_name = fields.Str(required=True, nullable=False, validate=not_empty_string)
    last_name = fields.Str(required=True, nullable=False, validate=not_empty_string)

