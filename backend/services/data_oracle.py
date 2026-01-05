import asyncio
from typing import Dict, List, Optional, AsyncIterator
from datetime import datetime, timedelta
import structlog
from fastapi import WebSocket
import numpy as np
import pandas as pd
from polygon import RESTClient as PolygonClient
from alpaca.data import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
import ccxt.async_support as ccxt

from backend.core.config import settings

logger = structlog.get_logger()

class DataOracle:
    def __init__(self):
        self.polygon_client = None
        self.alpaca_stock_client = None
        self.alpaca_crypto_client = None
        self.binance_client = None
        self.subscriptions: Dict[str, List[WebSocket]] = {}
        self.cache: Dict[str, any] = {}
        
    async def initialize(self):
        if settings.POLYGON_API_KEY:
            self.polygon_client = PolygonClient(settings.POLYGON_API_KEY)
        
        if settings.ALPACA_API_KEY:
            self.alpaca_stock_client = StockHistoricalDataClient(
                settings.ALPACA_API_KEY,
                settings.ALPACA_SECRET_KEY
            )
            self.alpaca_crypto_client = CryptoHistoricalDataClient()
        
        if settings.BINANCE_API_KEY:
            self.binance_client = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET,
                'enableRateLimit': True,
            })
        
        logger.info("data_oracle_initialized")
    
    async def get_quote(self, symbol: str) -> Optional[Dict]:
        try:
            request_params = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quote = self.alpaca_stock_client.get_stock_latest_quote(request_params)
            
            if symbol in quote:
                q = quote[symbol]
                return {
                    "symbol": symbol,
                    "bid": float(q.bid_price),
                    "ask": float(q.ask_price),
                    "bid_size": int(q.bid_size),
                    "ask_size": int(q.ask_size),
                    "timestamp": q.timestamp.isoformat()
                }
        except Exception as e:
            logger.error("get_quote_error", symbol=symbol, error=str(e))
        return None
    
    async def get_bars(self, symbol: str, timeframe: str, limit: int = 100) -> List[Dict]:
        try:
            tf_map = {
                "1M": TimeFrame.Minute,
                "5M": TimeFrame(5, "Min"),
                "15M": TimeFrame(15, "Min"),
                "1H": TimeFrame.Hour,
                "1D": TimeFrame.Day,
            }
            
            request_params = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=tf_map.get(timeframe, TimeFrame.Day),
                limit=limit
            )
            
            bars = self.alpaca_stock_client.get_stock_bars(request_params)
            
            result = []
            if symbol in bars:
                for bar in bars[symbol]:
                    result.append({
                        "timestamp": bar.timestamp.isoformat(),
                        "open": float(bar.open),
                        "high": float(bar.high),
                        "low": float(bar.low),
                        "close": float(bar.close),
                        "volume": int(bar.volume),
                        "vwap": float(bar.vwap) if bar.vwap else None,
                    })
            
            return result
        except Exception as e:
            logger.error("get_bars_error", symbol=symbol, error=str(e))
            return []
    
    async def get_historical(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: Optional[datetime],
        limit: int = 1000
    ) -> List[Dict]:
        return await self.get_bars(symbol, timeframe, limit)
    
    async def get_orderbook(self, symbol: str, depth: int = 20) -> Optional[Dict]:
        try:
            if self.binance_client and symbol.endswith("USDT"):
                orderbook = await self.binance_client.fetch_order_book(symbol, limit=depth)
                return {
                    "symbol": symbol,
                    "bids": [[float(p), float(q)] for p, q in orderbook['bids'][:depth]],
                    "asks": [[float(p), float(q)] for p, q in orderbook['asks'][:depth]],
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            logger.error("get_orderbook_error", symbol=symbol, error=str(e))
        return None
    
    async def get_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        try:
            if self.binance_client:
                trades = await self.binance_client.fetch_trades(symbol, limit=limit)
                return [
                    {
                        "timestamp": t['timestamp'],
                        "price": float(t['price']),
                        "size": float(t['amount']),
                        "side": t['side']
                    }
                    for t in trades
                ]
        except Exception as e:
            logger.error("get_trades_error", symbol=symbol, error=str(e))
        return []
    
    async def get_options_chain(self, symbol: str, expiration: Optional[str] = None) -> Optional[Dict]:
        return {
            "symbol": symbol,
            "expirations": ["2026-01-17", "2026-02-21", "2026-03-20"],
            "chains": []
        }
    
    async def calculate_greeks(self, symbol: str) -> Dict:
        from backend.utils.greeks_galaxy import calculate_all_greeks
        return await calculate_all_greeks(symbol)
    
    async def get_sentiment(self, symbol: str) -> Dict:
        return {
            "symbol": symbol,
            "sentiment_score": np.random.uniform(-1, 1),
            "news_count": np.random.randint(10, 100),
            "social_volume": np.random.randint(1000, 10000),
            "sources": ["twitter", "reddit", "news"]
        }
    
    async def get_alternative_data(self, symbol: str, source: str = "all") -> Dict:
        return {
            "symbol": symbol,
            "satellite_activity": np.random.uniform(0, 100),
            "web_traffic": np.random.randint(100000, 1000000),
            "employee_sentiment": np.random.uniform(-1, 1)
        }
    
    async def get_geopolitical_sentiment(self) -> List[Dict]:
        return [
            {
                "event": "Trade negotiations",
                "impact_score": 0.7,
                "affected_sectors": ["Technology", "Manufacturing"],
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    
    async def get_onchain_metrics(self, symbol: str) -> Dict:
        return {
            "symbol": symbol,
            "active_addresses": np.random.randint(10000, 100000),
            "transaction_volume": np.random.uniform(1e9, 1e12),
            "whale_transactions": np.random.randint(10, 100),
            "exchange_inflow": np.random.uniform(1e6, 1e9)
        }
    
    async def subscribe(self, symbol: str, websocket: WebSocket) -> str:
        subscription_id = f"{symbol}_{id(websocket)}"
        if symbol not in self.subscriptions:
            self.subscriptions[symbol] = []
        self.subscriptions[symbol].append(websocket)
        logger.info("websocket_subscribed", symbol=symbol, subscription_id=subscription_id)
        return subscription_id
    
    async def unsubscribe(self, subscription_id: str):
        logger.info("websocket_unsubscribed", subscription_id=subscription_id)
    
    async def stream_orderflow(self, symbol: str) -> AsyncIterator[Dict]:
        while True:
            yield {
                "symbol": symbol,
                "timestamp": datetime.utcnow().isoformat(),
                "delta": np.random.randint(-1000, 1000),
                "bid_volume": np.random.randint(1000, 10000),
                "ask_volume": np.random.randint(1000, 10000),
                "trades": np.random.randint(10, 100)
            }
            await asyncio.sleep(1)
    
    async def shutdown(self):
        if self.binance_client:
            await self.binance_client.close()
        logger.info("data_oracle_shutdown")
