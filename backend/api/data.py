from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.data_oracle import DataOracle
from backend.schemas.market import Bar, Quote, Trade, OrderBook, OptionsChain

router = APIRouter()
data_oracle = DataOracle()

class HistoricalRequest(BaseModel):
    symbol: str
    timeframe: str
    start: datetime
    end: Optional[datetime] = None
    limit: int = 1000

@router.get("/quote/{symbol}", response_model=Quote)
async def get_quote(symbol: str, current_user: User = Depends(get_current_user)):
    quote = await data_oracle.get_quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return quote

@router.get("/bars/{symbol}", response_model=List[Bar])
async def get_bars(
    symbol: str,
    timeframe: str = Query("1D", regex="^(1|5|15|30)M|[1-4]H|1D|1W$"),
    limit: int = Query(100, ge=1, le=5000),
    current_user: User = Depends(get_current_user)
):
    bars = await data_oracle.get_bars(symbol, timeframe, limit)
    return bars

@router.post("/historical", response_model=List[Bar])
async def get_historical_data(req: HistoricalRequest, current_user: User = Depends(get_current_user)):
    bars = await data_oracle.get_historical(req.symbol, req.timeframe, req.start, req.end, req.limit)
    return bars

@router.get("/orderbook/{symbol}", response_model=OrderBook)
async def get_orderbook(symbol: str, depth: int = Query(20, ge=1, le=100), current_user: User = Depends(get_current_user)):
    orderbook = await data_oracle.get_orderbook(symbol, depth)
    if not orderbook:
        raise HTTPException(status_code=404, detail="Order book not available")
    return orderbook

@router.get("/trades/{symbol}", response_model=List[Trade])
async def get_trades(symbol: str, limit: int = Query(100, ge=1, le=1000), current_user: User = Depends(get_current_user)):
    trades = await data_oracle.get_trades(symbol, limit)
    return trades

@router.get("/options/chain/{symbol}", response_model=OptionsChain)
async def get_options_chain(
    symbol: str,
    expiration: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    chain = await data_oracle.get_options_chain(symbol, expiration)
    if not chain:
        raise HTTPException(status_code=404, detail="Options chain not available")
    return chain

@router.get("/options/greeks/{symbol}")
async def get_options_greeks(symbol: str, current_user: User = Depends(get_current_user)):
    greeks = await data_oracle.calculate_greeks(symbol)
    return greeks

@router.get("/sentiment/{symbol}")
async def get_sentiment(symbol: str, current_user: User = Depends(get_current_user)):
    sentiment = await data_oracle.get_sentiment(symbol)
    return sentiment

@router.get("/alternative/{symbol}")
async def get_alternative_data(symbol: str, source: str = "all", current_user: User = Depends(get_current_user)):
    alt_data = await data_oracle.get_alternative_data(symbol, source)
    return alt_data

@router.get("/geopolitical")
async def get_geopolitical_events(current_user: User = Depends(get_current_user)):
    events = await data_oracle.get_geopolitical_sentiment()
    return events

@router.get("/crypto/onchain/{symbol}")
async def get_onchain_metrics(symbol: str, current_user: User = Depends(get_current_user)):
    metrics = await data_oracle.get_onchain_metrics(symbol)
    return metrics
