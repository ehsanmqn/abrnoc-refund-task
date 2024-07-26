from app.models import Transaction, db
from app.schemas import TransactionSchema


def create_transaction(data):
    schema = TransactionSchema()
    transaction_data = schema.load(data)
    transaction = Transaction(**transaction_data)

    db.session.add(transaction)
    db.session.commit()

    return schema.dump(transaction)


def get_transaction(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()

    if transaction:
        schema = TransactionSchema()
        return schema.dump(transaction)

    return None


def list_transactions(status_filter=None):
    schema = TransactionSchema(many=True)
    query = Transaction.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    transactions = query.all()

    return schema.dump(transactions)
