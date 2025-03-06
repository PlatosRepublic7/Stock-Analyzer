from database import SessionLocal, engine
from models import Base

from apscheduler.schedulers.blocking import BlockingScheduler
from api_client import store_stock_quote, store_av_time_series_ohlcv


def init_db():
    # Create all tables based on the models defined in Base
    Base.metadata.create_all(bind=engine)

def fetch_and_store(session):
    try:
        with open('symbols_master_list.txt') as f:
            file_lines = f.readlines()
            for line in file_lines:
                company_symbol_list = line.split('-')
                symbol = company_symbol_list[1].strip()
                #store_stock_quote(session, symbol)
                store_av_time_series_ohlcv(session, symbol)
        f.close()
    except Exception as e:
        print(f'File Parsing Error: {e}')


if __name__ == '__main__':
    init_db()
    session = SessionLocal()
    fetch_and_store(session)
    
    # scheduler = BlockingScheduler()

    # # Schedule job every five minutes
    # scheduler.add_job(fetch_and_store, 'interval', minutes=1)
    # print("Starting Scheduler... Press Ctrl+C to exit.")
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown(wait=False)
    #     print("Scheduler has been shut down.")
