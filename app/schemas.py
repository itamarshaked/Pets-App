from marshmallow import Schema, fields


class PetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    species = fields.Str(required=True)
    age = fields.Int(required=True)
    owner_id = fields.Int(dump_only=True)


class UserRegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str(load_default="user")


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    access_token = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    role = fields.Str()