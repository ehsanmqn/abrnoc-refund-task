import json
from kafka import KafkaConsumer
from app import create_app, db
from app.models import Refund
from app.tasks import process_refund

app = create_app()

consumer = KafkaConsumer(
    'refund_requests',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

with app.app_context():
    for message in consumer:
        data = message.value

        refund = Refund(
            transaction_id=data['transaction_id'],
            amount=data['amount'],
            reason=data['reason']
        )

        db.session.add(refund)
        db.session.commit()

        process_refund.delay(refund.id)
