from app import create_app, db
from consumer import KafkaConsumerService

app = create_app()
kafka_consumer = KafkaConsumerService(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    with app.app_context():
        kafka_consumer.start_consumer_thread()

    app.run(debug=True)
