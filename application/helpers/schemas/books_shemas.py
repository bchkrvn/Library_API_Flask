from marshmallow import Schema, fields, validates_schema, ValidationError

from .tools import not_empty_string


class BookSchema(Schema):
    title = fields.Str(required=True, nullable=False, validate=not_empty_string)
    author_id = fields.Int(required=False, nullable=False, validate=not_empty_string)
    author_first_name = fields.Str(required=False, nullable=False, validate=not_empty_string)
    author_last_name = fields.Str(required=False, nullable=False, validate=not_empty_string)
    reader_id = fields.Int(required=False, nullable=False, validate=not_empty_string)
    is_in_lib = fields.Bool(required=False, nullable=False, validate=not_empty_string)

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if 'is_in_lib' in data:
            if data['is_in_lib'] is False and 'reader_id' not in data:
                raise ValidationError("Didn't send reader_id if not in lib")

        if 'author_id' in data:
            pass
        elif 'author_first_name' in data and 'author_last_name' in data:
            pass
        else:
            raise ValidationError("Data must have author_id, or author_first_name and author_last_name keys")


class BookPatchSchema(Schema):
    title = fields.Str(required=False, nullable=False, validate=not_empty_string)
    author_id = fields.Int(required=False, nullable=False, validate=not_empty_string)
    author_first_name = fields.Str(required=False, nullable=False, validate=not_empty_string)
    author_last_name = fields.Str(required=False, nullable=False, validate=not_empty_string)
    reader_id = fields.Int(required=False, nullable=False, validate=not_empty_string)
    is_in_lib = fields.Bool(required=False, nullable=False, validate=not_empty_string)

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if 'is_in_lib' in data:
            if data['is_in_lib'] is False and 'reader_id' not in data:
                raise ValidationError("Didn't send reader_id if not in lib")

        if 'author_id' in data:
            pass
        elif 'author_first_name' in data and 'author_last_name' in data:
            pass
        elif 'author_first_name' in data or 'author_last_name' in data:
            raise ValidationError("Data must have author_id, or author_first_name and author_last_name keys")


class BookTransferSchema(Schema):
    reader_id = fields.Int(required=True, nullable=False, validate=not_empty_string)
    book_id = fields.Int(required=True, nullable=False, validate=not_empty_string)
