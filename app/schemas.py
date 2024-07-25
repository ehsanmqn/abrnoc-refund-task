from marshmallow import Schema, fields


class RefundSchema(Schema):
    id = fields.Int()
    transaction_id = fields.Str()
    amount = fields.Float()
    reason = fields.Str()
    status = fields.Str()
