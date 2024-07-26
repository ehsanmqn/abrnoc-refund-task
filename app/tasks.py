from datetime import datetime, timedelta
from celery_worker import celery
import requests

from app import db
from app.models import Transaction, Refund


@celery.task
def process_refund(refund_id):
    with celery.app.app_context():
        refund = Refund.query.get(refund_id)

        if refund and refund.status == 'pending':
            response = requests.post('http://external-api/refund', json={
                "transaction_id": refund.transaction_id,
                "amount": refund.amount,
                "reason": refund.reason
            })

            if response.status_code == 200:
                refund.status = 'confirmed'
                db.session.commit()


@celery.task
def check_status():
    with celery.app.app_context():

        # Survey transactions
        transactions = Transaction.query.filter_by(status='pending').all()
        for transaction in transactions:
            if datetime.utcnow() - transaction.created_at > timedelta(hours=1):
                response = requests.get(f'http://external-api/payment/status?transaction_id={transaction.id}')

                if response.status_code == 200:
                    status_data = response.json()
                    transaction.status = status_data['status']

                    if status_data['status'] == 'failed':
                        refund_response = requests.post('http://external-api/refund', json={
                            "transaction_id": transaction.id,
                            "amount": transaction.amount,
                            "reason": "payment failed"
                        })

                        if refund_response.status_code == 200:
                            refund_data = refund_response.json()

                            refund = Refund(
                                refund_id=refund_data['refund_id'],
                                transaction_id=transaction.id,
                                amount=transaction.amount,
                                reason="payment failed",
                                status=refund_data['status']
                            )

                            db.session.add(refund)
                            db.session.commit()

        # Survey refunds
        refunds = Refund.query.filter_by(status='pending').all()
        for refund in refunds:
            response = requests.get(f'http://external-api/refund/status?refund_id={refund.id}')

            if response.status_code == 200:
                status_data = response.json()
                refund.status = status_data['status']
                db.session.commit()
