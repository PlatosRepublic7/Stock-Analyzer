from database import SessionLocal, engine
from models import Base

from apscheduler.schedulers.blocking import BlockingScheduler
from finnhub_client import store_stock_quote


def init_db():
    # Create all tables based on the models defined in Base
    Base.metadata.create_all(bind=engine)

def fetch_and_store(session):
    store_stock_quote(session, "AAPL")


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
