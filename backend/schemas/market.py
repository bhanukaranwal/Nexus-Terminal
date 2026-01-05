from pydantic import BaseModel
from datetime import datetime

class Quote(BaseModel):
    symbol: str
    bid: float
    ask: float
    bid_size: int
    ask_size: int
    timestamp: str

class Bar(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    vwap: float | None

class Trade(BaseModel):
    timestamp: str
    price: float
    size: float
    side: str

class OrderBook(BaseModel):
    symbol: str
    bids: list
    asks: list
    timestamp: str

class OptionsChain(BaseModel):
    symbol: str
    expirations: list[str]
    chains: list
