from marshmallow import Schema, fields


class RefundSchema(Schema):
    id = fields.Int()
    transaction_id = fields.Str()
    amount = fields.Float()
    reason = fields.Str()
    status = fields.Str()


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Str(required=True)
    transaction_id = fields.Str(required=True)
    amount = fields.Float(required=True)
    description = fields.Str()
    payment_method = fields.Str()
    status = fields.Str()
