from app.models import Refund


def get_refund_by_id(refund_id):
    return Refund.query.get(refund_id)


def get_all_refunds():
    return Refund.query.all()


def filter_refunds(transaction_id=None, status=None):
    query = Refund.query
    if transaction_id:
        query = query.filter_by(transaction_id=transaction_id)
    if status:
        query = query.filter_by(status=status)
    return query.all()
