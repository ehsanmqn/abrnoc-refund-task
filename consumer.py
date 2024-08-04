import asyncio
import json
from threading import Thread
from aiokafka import AIOKafkaConsumer
from flask import current_app as app
from concurrent.futures import ThreadPoolExecutor

from app import db
from app.models import Transaction

executor = ThreadPoolExecutor(max_workers=10)


async def handle_message(data):
    transaction = Transaction(
        transaction_id=data['transaction_id'],
        amount=data['amount'],
        description=data['description'],
        payment_method=data['payment_method']
    )
    db.session.add(transaction)

    await asyncio.get_event_loop().run_in_executor(executor, db.session.commit)


async def consume_messages():
    consumer = AIOKafkaConsumer(
        app.config['REFUND_TOPIC'],
        bootstrap_servers=app.config['KAFKA_BOOTSTRAP_SERVERS'],
        group_id='my-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    await consumer.start()

    try:
        async for message in consumer:
            await handle_message(message.value)
    finally:
        await consumer.stop()


def start_consumer_loop(app):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with app.app_context():
        loop.run_until_complete(consume_messages())


def start_consumer_thread(app):
    t = Thread(target=start_consumer_loop, args=(app,))
    t.start()
