import requests
from models import Symbol, Quote, AlphaVantageQuote
import os

from datetime import datetime, timezone


FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/"

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/"


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
        
        try:
            # Create a new Symbol object
            symbol_obj = Symbol(symbol=symbol_str, description=description, display_symbol=display_symbol, type=type)
            session.add(symbol_obj)
            session.commit()
            session.refresh(symbol_obj)
        except Exception as e:
            session.rollback()
            print(f"Error storing new Symbol {symbol_str}: {e}")
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
        print(f"\nCreated a New Symbol: {symbol_obj.symbol} with id {symbol_obj.id}")
    else:
        print(f"\nFound existing Symbol: {symbol_obj.symbol} with id {symbol_obj.id}")

    try:
        # data['c'] represents the current price
        current_price = data.get('c')
        change = data.get('d')
        percent_change = data.get('dp')
        high_price = data.get('h')
        low_price = data.get('l')
        open_price = data.get('o')
        previous_close = data.get('pc')
        timestamp = data.get('t')

        new_quote = Quote(
            symbol_id=symbol_obj.id,
            current_price=current_price,
            change=change,
            percent_change=percent_change,
            high_price=high_price,
            low_price=low_price,
            open_price=open_price,
            prev_close=previous_close,
            timestamp=timestamp
        )
        session.add(new_quote)
        session.commit()
        print(f"\nStored Quote for {symbol} at {datetime.now(timezone.utc)} with id {new_quote.id}:\nCurrent Price: {current_price}\nChange: {change}\nPercent Change: {percent_change}\nHigh Price: {high_price}\nLow Price: {low_price}\nOpen Price: {open_price}\nPrevious Close: {previous_close}")
    except Exception as e:
        session.rollback()
        print(f"Error storing data for {symbol}: {e}")
    finally:
        session.close()


def get_av_time_series_data(symbol):
    params = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "apikey": ALPHA_VANTAGE_API_KEY}
    response = requests.get(ALPHA_VANTAGE_URL + "query", params=params)
    response.raise_for_status()
    return response.json()


def store_av_time_series_ohlcv(session, symbol):
    symbol_obj, created = get_or_create_symbol(session, symbol)
    if created:
        print(f"\nCreated a New Symbol: {symbol_obj.symbol} - {symbol_obj.description} with id {symbol_obj.id}")
    else:
        print(f"\nFound existing Symbol: {symbol_obj.symbol} - {symbol_obj.description} with id {symbol_obj.id}")

    data = get_av_time_series_data(symbol)
    try:
        time_series_data = data.get('Time Series (Daily)')
        for key, value in time_series_data.items():
            open = value['1. open']
            high = value['2. high']
            low = value['3. low']
            close = value['4. close']
            volume = value['5. volume']
            date = key

            av_obj = session.query(AlphaVantageQuote).filter_by(date=date).first()
            if not av_obj:
                av_quote = AlphaVantageQuote(
                    symbol_id=symbol_obj.id,
                    open=open,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    date=date
                )

                session.add(av_quote)
                session.commit()
                print(f'\nStored AlphaVantage Quote for {symbol} at {datetime.now(timezone.utc)} with id {av_quote.id}:\nOpen: {open}\nHigh: {high}\nLow: {low}\nClose: {close}\nVolume: {volume}\n')
            else:
                break
    except Exception as e:
        session.rollback()
        print(f'Error storing data for {symbol}: {e}')
    finally:
        session.close()
