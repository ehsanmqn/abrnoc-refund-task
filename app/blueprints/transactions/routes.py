from flask import Blueprint, request, jsonify
from .services import get_transaction, list_transactions, get_failed_transactions, get_incomplete_transactions

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/transactions', methods=['GET'])
def list_all_transactions():
    status_filter = request.args.get('status')
    transactions = list_transactions(status_filter)

    return jsonify(transactions)


@transactions_bp.route('/transactions/<transaction_id>', methods=['GET'])
def get_specific_transaction(transaction_id):
    transaction = get_transaction(transaction_id)

    if transaction:
        return jsonify(transaction)

    return jsonify({'error': 'Transaction not found'}), 404


@transactions_bp.route('/transactions/failed', methods=['GET'])
def list_failed_transactions():
    transactions = get_failed_transactions()

    return jsonify(transactions)


@transactions_bp.route('/transactions/incomplete', methods=['GET'])
def list_incomplete_transactions():
    transactions = get_incomplete_transactions()

    return jsonify(transactions)
