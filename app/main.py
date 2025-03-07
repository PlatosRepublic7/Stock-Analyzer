from database.database import SessionLocal, engine
from database.models import Base

from apscheduler.schedulers.blocking import BlockingScheduler
from api_client import store_stock_quote, store_av_time_series_ohlcv
from forecast_models.forecast_processer import update_forecast_data


class StockSymbols:
    def __init__(self, file_path=None):
        self.symbols = []
        self.file_path = file_path


    def generate_symbols(self):
        try:
            with open(self.file_path) as f:
                file_lines = f.readlines()
                for line in file_lines:
                    company_symbol_list = line.split('-')
                    symbol = company_symbol_list[1].strip()
                    if symbol not in self.symbols:
                        self.symbols.append(symbol)
            f.close()
        except Exception as e:
            print(f'File at {self.file_path} has encountered a parsing error: {e}')


    def get_symbol(self, symbol):
        for s in self.symbols:
            if s == symbol:
                return s


def init_db():
    # Create all tables based on the models defined in Base
    Base.metadata.create_all(bind=engine)

def fetch_and_store(session, stock_symbols):
    for symbol in stock_symbols:
        store_av_time_series_ohlcv(session, symbol)


if __name__ == '__main__':
    init_db()
    session = SessionLocal()
    stock_symbols = StockSymbols('symbols_master_list.txt')
    stock_symbols.generate_symbols()
    update_forecast_data(session, stock_symbols)
    # fetch_and_store(session, stock_symbols)
    
    # scheduler = BlockingScheduler()

    # # Schedule job every five minutes
    # scheduler.add_job(fetch_and_store, 'interval', minutes=1)
    # print("Starting Scheduler... Press Ctrl+C to exit.")
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown(wait=False)
    #     print("Scheduler has been shut down.")
