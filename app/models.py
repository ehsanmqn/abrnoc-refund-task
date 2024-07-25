from app import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), index=True)
    amount = db.Column(db.Float)
    payment_method = db.Column(db.String(64))
    description = db.Column(db.String(128))
    status = db.Column(db.String(64), default='pending')


class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(64), index=True)
    amount = db.Column(db.Float)
    reason = db.Column(db.String(128))
    status = db.Column(db.String(64), default='pending')
