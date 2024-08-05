import requests
from datetime import datetime, timedelta
from requests.exceptions import RequestException

from celery_worker import celery
from app import db
from app.models import Transaction, Refund


@celery.task(name='app.tasks.check_status')
def check_status():
    try:
        # Survey transactions
        transactions = Transaction.query.filter_by(status='pending').all()
        for transaction in transactions:
            if datetime.utcnow() - transaction.created_at > timedelta(hours=1):
                try:
                    response = requests.get(f'http://external-api/payment/status?transaction_id={transaction.id}')
                    response.raise_for_status()
                    status_data = response.json()
                    transaction.status = status_data['status']

                    if status_data['status'] == 'failed':
                        try:
                            refund_response = requests.post('http://external-api/refund', json={
                                "transaction_id": transaction.id,
                                "amount": transaction.amount,
                                "reason": "payment failed"
                            })
                            refund_response.raise_for_status()
                            refund_data = refund_response.json()

                            refund = Refund(
                                refund_id=refund_data['refund_id'],
                                transaction_id=transaction.id,
                                amount=transaction.amount,
                                reason="payment failed",
                                status=refund_data['status']
                            )

                            db.session.add(refund)
                            db.session.flush()
                            db.session.commit()

                        except RequestException as e:
                            print(f"Refund request failed: {e}")

                except RequestException as e:
                    print(f"Status check request failed: {e}")

        # Survey refunds
        refunds = Refund.query.filter_by(status='pending').all()
        for refund in refunds:
            try:
                response = requests.get(f'http://external-api/refund/status?refund_id={refund.id}')
                response.raise_for_status()
                status_data = response.json()
                refund.status = status_data['status']
                db.session.commit()

            except RequestException as e:
                print(f"Refund status check request failed: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
