from flask import Blueprint

transactions_bp = Blueprint('transactions', __name__)

from app.blueprints.transactions import routes
