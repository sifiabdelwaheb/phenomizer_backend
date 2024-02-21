from marshmallow import Schema, fields
from marshmallow.validate import Length


class ProductSchema(Schema):
    useremail = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(4, 20), load_only=True)
    # username = fields.Str(required=True, validate=Length(2, 20))
    # øadresse = fields.Str(required=True, validate=Length(5, 40))
