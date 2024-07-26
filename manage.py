import os
from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

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


@cli.command("migrate")
def migrate():
    with app.app_context():
        from flask_migrate import upgrade
        upgrade()

    print("Migrations completed.")


@cli.command("upgrade")
def upgrade():
    with app.app_context():
        from flask_migrate import migrate as migrate_command
        migrate_command()

    print("Database upgraded.")


@cli.command("init-db")
def init_db():
    create_db()
    migrate()
    upgrade()

    print("Database initialized and migrations applied.")


if __name__ == "__main__":
    cli()
