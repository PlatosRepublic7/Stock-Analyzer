from app.db.models import Symbol, AlphaVantageQuote
from .arima_model import ARIMAModel
import pandas as pd


def update_forecast_data(session, stock_symbols):
    '''
    Driver funtion for updating forcast data within the database
    '''
    df_dict = {}
    for symbol in stock_symbols.symbols:
        # Get all AlphaVantageQuote object(s) up to current date by Symbol, and create a dataframe with all needed data
        ts_df = get_latest_data(session, symbol)
        
        # Store each dataframe into a dictionary for further processing - keys are the stock symbol
        if ts_df is not None:
            df_dict[symbol] = ts_df


def get_latest_data(session, symbol_str: str) -> pd.DataFrame | None:
    '''
    Retrieve latest AlphaVantageQuote data for symbol
    '''
    av_obj_data = []
    try:
        # Query database for Symbol
        symbol_obj = session.query(Symbol).filter_by(symbol=symbol_str).first()
        if symbol_obj is not None:
            # Use this Symbol to query for all related AlphaVantageQuote objects, ordered by date, descending
            time_series_data = session.query(AlphaVantageQuote).filter_by(symbol_id=symbol_obj.id).order_by(AlphaVantageQuote.date.desc()).all()
            
            # If time_series_data is None, return None
            if not time_series_data:
                return None

            # Loop through each returned object, and convert to dictionary
            for av_obj in time_series_data:
                av_obj_dict = {
                    'symbol': symbol_obj.symbol,
                    'id': av_obj.id,
                    'open': av_obj.open,
                    'high': av_obj.high,
                    'low': av_obj.low,
                    'close': av_obj.close,
                    'volume': av_obj.volume,
                    'date': av_obj.date
                }
                av_obj_data.append(av_obj_dict)

            # Create a dataframe from the list of AlphaVantageQuote dictionaries
            df = pd.DataFrame(av_obj_data, columns=['symbol', 'id', 'open', 'high', 'low', 'close', 'volume', 'date'])
            
            return df
        else:
            return None
    except Exception as e:
        session.rollback()
        print(f'Error retreiving data for {symbol_str}: {e}')