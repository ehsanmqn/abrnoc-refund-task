from flask import request, jsonify
from app.schemas import RefundSchema
from . import refunds_bp
from .services import get_refund_by_id, get_all_refunds, filter_refunds

refund_schema = RefundSchema()
refunds_schema = RefundSchema(many=True)


@refunds_bp.route('/refund/<int:refund_id>', methods=['GET'])
def get_refund(refund_id):
    refund = get_refund_by_id(refund_id)
    if refund:
        return refund_schema.jsonify(refund)
    return jsonify({"error": "Refund not found"}), 404


@refunds_bp.route('/refunds', methods=['GET'])
def get_refunds():
    refunds = get_all_refunds()
    return refunds_schema.jsonify(refunds)


@refunds_bp.route('/refunds/filter', methods=['GET'])
def filter_refunds_endpoint():
    transaction_id = request.args.get('transaction_id')
    status = request.args.get('status')
    refunds = filter_refunds(transaction_id, status)
    return refunds_schema.jsonify(refunds)
