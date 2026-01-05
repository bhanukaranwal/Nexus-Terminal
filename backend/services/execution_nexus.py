from typing import Dict, List, Optional
from datetime import datetime
import structlog
from enum import Enum
import asyncio

logger = structlog.get_logger()

class OrderStatus(str, Enum):
    PENDING = "pending"
    FILLED = "filled"
    PARTIAL = "partial"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class ExecutionNexus:
    def __init__(self):
        self.orders: Dict[str, Dict] = {}
        self.positions: Dict[str, Dict] = {}
        
    async def place_order(
        self,
        user_id: int,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "gtc",
        broker: str = "alpaca"
    ) -> Dict:
        order_id = f"ORD-{datetime.utcnow().timestamp()}"
        
        order = {
            "id": order_id,
            "user_id": user_id,
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "quantity": quantity,
            "price": price,
            "stop_price": stop_price,
            "time_in_force": time_in_force,
            "broker": broker,
            "status": OrderStatus.PENDING,
            "filled_qty": 0,
            "avg_fill_price": 0,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.orders[order_id] = order
        
        asyncio.create_task(self._simulate_fill(order_id))
        
        logger.info("order_placed", order_id=order_id, symbol=symbol, side=side)
        return order
    
    async def _simulate_fill(self, order_id: str):
        await asyncio.sleep(2)
        if order_id in self.orders:
            self.orders[order_id]["status"] = OrderStatus.FILLED
            self.orders[order_id]["filled_qty"] = self.orders[order_id]["quantity"]
            self.orders[order_id]["avg_fill_price"] = self.orders[order_id].get("price", 100.0)
            logger.info("order_filled", order_id=order_id)
    
    async def get_orders(
        self,
        user_id: int,
        status: Optional[OrderStatus] = None,
        symbol: Optional[str] = None
    ) -> List[Dict]:
        orders = [o for o in self.orders.values() if o["user_id"] == user_id]
        if status:
            orders = [o for o in orders if o["status"] == status]
        if symbol:
            orders = [o for o in orders if o["symbol"] == symbol]
        return orders
    
    async def get_order(self, order_id: str, user_id: int) -> Optional[Dict]:
        order = self.orders.get(order_id)
        if order and order["user_id"] == user_id:
            return order
        return None
    
    async def update_order(self, order_id: str, order_update: Dict, user_id: int) -> Dict:
        order = self.orders.get(order_id)
        if not order or order["user_id"] != user_id:
            raise ValueError("Order not found")
        
        order.update(order_update.dict(exclude_unset=True))
        logger.info("order_updated", order_id=order_id)
        return order
    
    async def cancel_order(self, order_id: str, user_id: int):
        order = self.orders.get(order_id)
        if not order or order["user_id"] != user_id:
            raise ValueError("Order not found")
        
        order["status"] = OrderStatus.CANCELLED
        logger.info("order_cancelled", order_id=order_id)
    
    async def place_bracket_order(
        self,
        user_id: int,
        symbol: str,
        side: str,
        quantity: float,
        entry_price: float,
        take_profit: float,
        stop_loss: float
    ) -> Dict:
        entry = await self.place_order(user_id, symbol, side, "limit", quantity, entry_price)
        
        return {
            "bracket_id": f"BKT-{datetime.utcnow().timestamp()}",
            "entry_order": entry,
            "take_profit_price": take_profit,
            "stop_loss_price": stop_loss
        }
    
    async def smart_route(self, user_id: int, order: Dict) -> Dict:
        order["broker"] = "alpaca"
        return await self.place_order(user_id, **order)
    
    async def get_positions(self, user_id: int, broker: Optional[str] = None) -> List[Dict]:
        positions = [p for p in self.positions.values() if p.get("user_id") == user_id]
        if broker:
            positions = [p for p in positions if p.get("broker") == broker]
        return positions
    
    async def get_position(self, user_id: int, symbol: str) -> Optional[Dict]:
        for pos in self.positions.values():
            if pos.get("user_id") == user_id and pos.get("symbol") == symbol:
                return pos
        return None
    
    async def close_position(self, user_id: int, symbol: str, quantity: Optional[float] = None) -> Dict:
        position = await self.get_position(user_id, symbol)
        if not position:
            raise ValueError("Position not found")
        
        close_qty = quantity or position.get("quantity", 0)
        side = "sell" if position.get("side") == "long" else "buy"
        
        return await self.place_order(user_id, symbol, side, "market", close_qty)
    
    async def get_portfolio_summary(self, user_id: int) -> Dict:
        return {
            "user_id": user_id,
            "total_value": 100000.0,
            "cash": 50000.0,
            "equity": 50000.0,
            "buying_power": 100000.0,
            "day_pnl": 1250.0,
            "total_pnl": 5000.0
        }
    
    async def calculate_performance_metrics(self, user_id: int, period: str) -> Dict:
        return {
            "sharpe_ratio": 1.5,
            "sortino_ratio": 2.0,
            "max_drawdown": 0.15,
            "win_rate": 0.62,
            "profit_factor": 1.8,
            "total_return": 0.25
        }
    
    async def get_asset_allocation(self, user_id: int) -> Dict:
        return {
            "equities": 0.60,
            "options": 0.15,
            "crypto": 0.20,
            "cash": 0.05
        }
    
    async def get_pnl_history(self, user_id: int, period: str) -> List[Dict]:
        return [
            {"date": "2026-01-01", "pnl": 500},
            {"date": "2026-01-02", "pnl": 750},
            {"date": "2026-01-03", "pnl": -200},
            {"date": "2026-01-04", "pnl": 1000},
        ]
