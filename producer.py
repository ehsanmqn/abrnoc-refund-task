import random

from confluent_kafka import Producer
import json
from datetime import datetime

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(conf)

message = {
    "user_id": "user123",
    "service_id": "payment_service",
    "timestamp": datetime.now().isoformat(),
    "request_details": "New payment",
    "transaction_id": str(random.randint(1000, 9999)),
    "status": "confirmed",
    "amount": "100",
    "payment_method": "Stripe",
    "description": "Payment verified"
}

message_json = json.dumps(message)

topic = 'refund_requests'


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


producer.produce(topic, value=message_json, callback=delivery_report)
producer.flush()
