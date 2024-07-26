import os
from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()

cli = FlaskGroup(app)


@cli.command("create-db")
def create_db():
    with app.app_context():
        db.create_all()
    print("Database created.")


@cli.command("drop-db")
def drop_db():
    with app.app_context():
        db.drop_all()
    print("Database dropped.")


if __name__ == "__main__":
    cli()
