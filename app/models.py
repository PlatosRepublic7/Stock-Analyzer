from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column, DeclarativeBase

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine and the session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for class definitions
class Base(DeclarativeBase):
    pass

# Models
class Symbol(Base):
    __tablename__ = 'symbols'
    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol = mapped_column(String, index=True)
    name = mapped_column(String)
    created_at = mapped_column(DateTime)
    updated_at = mapped_column(DateTime)
    deleted_at = mapped_column(DateTime)
    children = relationship("Quote", back_populates="symbols", cascade="all, delete", passive_deletes=True)


class Quote(Base):
    __tablename__ = 'quotes'
    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol_id = mapped_column(Integer, ForeignKey('symbols.id', ondelete='CASCADE'))
    symbol = relationship("Symbol", back_populates="quotes")
    current_price =  mapped_column(Float)
    high_price = mapped_column(Float)
    low_price = mapped_column(Float)
    open_price = mapped_column(Float)
    prev_close = mapped_column(Float)
    timestamp = mapped_column(Integer)
    created_at = mapped_column(DateTime)
    updated_at = mapped_column(DateTime)
    deleted_at = mapped_column(DateTime)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)