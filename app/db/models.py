from sqlalchemy import Integer, String, DateTime, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, DeclarativeBase
from datetime import datetime, timezone

# Base model for class definitions
class Base(DeclarativeBase):
    pass

# Models
class Symbol(Base):
    __tablename__ = "symbols"
    id = mapped_column(Integer, primary_key=True, index=True)
    symbol = mapped_column(String, index=True)
    description = mapped_column(String, nullable=True)
    display_symbol = mapped_column(String, nullable=True)
    type = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = mapped_column(DateTime, nullable=True)
    quotes = relationship("Quote", back_populates="symbol", cascade="all, delete", passive_deletes=True)
    alpha_vantage_quotes = relationship("AlphaVantageQuote", back_populates="symbol", cascade="all, delete", passive_deletes=True)


    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'description': self.description,
            'display_symbol': self.display_symbol,
            'type': self.type
        }


class Quote(Base):
    __tablename__ = "quotes"
    id = mapped_column(Integer, primary_key=True, index=True)
    symbol_id = mapped_column(Integer, ForeignKey('symbols.id', ondelete='CASCADE'))
    symbol = relationship("Symbol", back_populates="quotes")
    current_price =  mapped_column(Float)
    change = mapped_column(Float, nullable=True)
    percent_change = mapped_column(Float, nullable=True)
    high_price = mapped_column(Float)
    low_price = mapped_column(Float)
    open_price = mapped_column(Float)
    prev_close = mapped_column(Float)
    timestamp = mapped_column(Integer)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = mapped_column(DateTime, nullable=True)


class AlphaVantageQuote(Base):
    __tablename__ = 'alpha_vantage_quotes'
    id = mapped_column(Integer, primary_key=True, index=True)
    symbol_id = mapped_column(Integer, ForeignKey('symbols.id', ondelete='CASCADE'))
    symbol = relationship("Symbol", back_populates="alpha_vantage_quotes")
    open = mapped_column(Float, nullable=True)
    high = mapped_column(Float, nullable=True)
    low = mapped_column(Float, nullable=True)
    close = mapped_column(Float, nullable=True)
    volume = mapped_column(Integer, nullable=True)
    date = mapped_column(Date, nullable=True)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


    def to_dict(self):
        return {
            'id': self.id,
            'symbol_id': self.symbol_id,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'date': self.date
        }