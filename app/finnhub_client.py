import requests
from datetime import datetime
from models import Symbol, Quote
from dotenv import load_dotenv
import os


FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/"


def get_or_create_symbol(session, symbol_str):
    symbol_obj = session.query(Symbol).filter_by(symbol=symbol_str).first()
    if symbol_obj:
        # Found an existing symbol
        return symbol_obj, False
    else:
        # Go to Symbol Lookup endpoint on finnhub, and get the name of the company
        params = {"q": symbol_str, "token": FINNHUB_API_KEY}
        response = requests.get(FINNHUB_URL + "search", params=params)
        response.raise_for_status()
        data = response.json()

        if data['count'] == 0:
            return None, False
        else:
            for result in data['result']:
                if result['symbol'] == symbol_str:
                    description = result['description']
                    display_symbol = result['displaySymbol']
                    type = result['type']
                    break
        
        # Create a new Symbol object
        symbol_obj = Symbol(symbol=symbol_str, description=description, display_symbol=display_symbol, type=type)
        session.add(symbol_obj)
        session.commit()
        session.refresh(symbol_obj)
        return symbol_obj, True


def get_stock_quote(symbol):
    params = {"symbol": symbol, "token": FINNHUB_API_KEY}
    response = requests.get(FINNHUB_URL + "quote", params=params)
    response.raise_for_status()
    return response.json()


def store_stock_quote(session, symbol):
    data = get_stock_quote(symbol)
    symbol_obj, created = get_or_create_symbol(session, symbol)
    if created:
        print(f"Created a New Symbol: {symbol_obj.symbol} with id {symbol_obj.id}")
    else:
        print(f"Found existing Symbol: {symbol_obj.symbol} with id {symbol_obj.id}")

    try:
        # data['c'] represents the current price
        price = data.get('c')
        change = data.get('d')
        percent_change = data.get('dp')
        high_price = data.get('h')
        low_price = data.get('l')
        open_price = data.get('o')
        previous_close = data.get('pc')
        timestamp = data.get('t')

        new_quote = Quote(
            symbol_id=symbol_obj.id,
            current_price=price,
            high_price=high_price,
            low_price=low_price,
            open_price=open_price,
            prev_close=previous_close,
            timestamp=timestamp
        )
        session.add(new_quote)
        session.commit()
        print(f"Stored {symbol}:\nCurrent Price:{price}\nHigh Price:{high_price}\nLow Price:{low_price}\nOpen Price:{open_price}\nPrevious Close:{previous_close}")
    except Exception as e:
        session.rollback()
        print(f"Error storing data for {symbol}: {e}")
    finally:
        session.close()

