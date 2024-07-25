from flask import Blueprint

refunds_bp = Blueprint('refunds', __name__)

from app.blueprints.refunds import routes
