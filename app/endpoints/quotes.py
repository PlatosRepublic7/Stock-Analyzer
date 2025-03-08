from flask import Blueprint, jsonify, request, g
from app.db.models import Symbol, AlphaVantageQuote

quotes_bp = Blueprint('quotes', __name__)

@quotes_bp.route('/quote', methods=['GET'])
def get_quote():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'Error': "Missing required query parameter 'symbol'"}), 400
    
    # Process the request if symbol parameter is present
    session = g.get('session')
    try:
        symbol_obj = session.query(Symbol).filter_by(symbol=symbol).first()
        av_quotes = session.query(AlphaVantageQuote).filter_by(symbol_id=symbol_obj.id).order_by(AlphaVantageQuote.date.desc()).all()
        av_quotes_data = [av_quote.to_dict() for av_quote in av_quotes]
        return jsonify(av_quotes_data)
    except Exception as e:
        return jsonify({'Error': f'{e}'})