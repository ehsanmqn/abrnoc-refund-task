from app import create_app, db
from consumer import start_consumer_thread

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    with app.app_context():
        start_consumer_thread(app)

    app.run(debug=True)
