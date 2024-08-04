from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import Migrate, migrate as migrate_command, upgrade

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


@cli.command("migrate-db")
def migrate_db():
    with app.app_context():
        migrate_command()
    print("Migrations completed.")


@cli.command("upgrade-db")
def upgrade_db():
    with app.app_context():
        upgrade()
    print("Database upgraded.")


if __name__ == "__main__":
    cli()
