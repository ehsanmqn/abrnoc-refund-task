from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app.blueprints.refunds import refunds_bp
    from app.blueprints.transactions import transactions_bp

    app.register_blueprint(refunds_bp, url_prefix='/api')
    app.register_blueprint(transactions_bp, url_prefix='/api')

    return app
