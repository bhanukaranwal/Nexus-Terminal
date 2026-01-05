from typing import List, Optional
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.execution_nexus import ExecutionNexus
from backend.schemas.order import Order, OrderCreate, OrderUpdate, OrderStatus

router = APIRouter()
execution_nexus = ExecutionNexus()

class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"
    BRACKET = "bracket"
    OCO = "oco"
    ICEBERG = "iceberg"
    TWAP = "twap"
    VWAP = "vwap"
    ADAPTIVE = "adaptive"
    AGENTIC = "agentic"

class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

@router.post("/", response_model=Order, status_code=201)
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user)):
    try:
        executed_order = await execution_nexus.place_order(
            user_id=current_user.id,
            symbol=order.symbol,
            side=order.side,
            order_type=order.order_type,
            quantity=order.quantity,
            price=order.price,
            stop_price=order.stop_price,
            time_in_force=order.time_in_force,
            broker=order.broker
        )
        return executed_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Order])
async def get_orders(
    status: Optional[OrderStatus] = None,
    symbol: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    orders = await execution_nexus.get_orders(user_id=current_user.id, status=status, symbol=symbol)
    return orders

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    order = await execution_nexus.get_order(order_id, user_id=current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}", response_model=Order)
async def update_order(order_id: str, order_update: OrderUpdate, current_user: User = Depends(get_current_user)):
    try:
        updated_order = await execution_nexus.update_order(order_id, order_update, user_id=current_user.id)
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{order_id}")
async def cancel_order(order_id: str, current_user: User = Depends(get_current_user)):
    try:
        await execution_nexus.cancel_order(order_id, user_id=current_user.id)
        return {"status": "cancelled", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bracket")
async def create_bracket_order(
    symbol: str,
    side: OrderSide,
    quantity: float,
    entry_price: float,
    take_profit: float,
    stop_loss: float,
    current_user: User = Depends(get_current_user)
):
    try:
        bracket = await execution_nexus.place_bracket_order(
            user_id=current_user.id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=entry_price,
            take_profit=take_profit,
            stop_loss=stop_loss
        )
        return bracket
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/smart-route")
async def smart_route_order(order: OrderCreate, current_user: User = Depends(get_current_user)):
    try:
        routed_order = await execution_nexus.smart_route(
            user_id=current_user.id,
            order=order
        )
        return routed_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
