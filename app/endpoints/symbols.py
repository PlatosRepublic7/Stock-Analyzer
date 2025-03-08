from flask import Blueprint, jsonify, request, g
from app.db.models import Symbol

symbols_bp = Blueprint('symbols', __name__)

@symbols_bp.route('/symbols', methods=['GET'])
def get_symbols():
    session = g.get('session')
    symbols = session.query(Symbol).all()
    symbols_data = [symbol.to_dict() for symbol in symbols]
    return jsonify(symbols_data)