import asyncio
import json
from threading import Thread
from aiokafka import AIOKafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from app import db
from app.models import Transaction


class KafkaConsumerService:
    def __init__(self, app):
        self.app = app
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def handle_message(self, data):
        with self.app.app_context():
            try:
                transaction = Transaction(
                    user_id=data['user_id'],
                    transaction_id=data['transaction_id'],
                    amount=data['amount'],
                    description=data['description'],
                    payment_method=data['payment_method'],
                    status=data['status']
                )
                db.session.add(transaction)
                db.session.commit()
                print(f"New transaction has been added to the database. Transaction ID: {data['transaction_id']}")
            except Exception as e:
                print(f"Error processing message: {e}")
                db.session.rollback()

    async def consume_messages(self):
        consumer = AIOKafkaConsumer(
            self.app.config['REFUND_TOPIC'],
            bootstrap_servers=self.app.config['KAFKA_BOOTSTRAP_SERVERS'],
            group_id='my-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        await consumer.start()

        try:
            async for message in consumer:
                await self.handle_message(message.value)
        except Exception as e:
            print(f"Error consuming messages: {e}")
        finally:
            await consumer.stop()

    def start_consumer_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with self.app.app_context():
            loop.run_until_complete(self.consume_messages())

    def start_consumer_thread(self):
        t = Thread(target=self.start_consumer_loop)
        t.start()
