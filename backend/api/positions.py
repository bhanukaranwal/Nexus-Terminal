from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.execution_nexus import ExecutionNexus
from backend.schemas.position import Position

router = APIRouter()
execution_nexus = ExecutionNexus()

@router.get("/", response_model=List[Position])
async def get_positions(broker: Optional[str] = None, current_user: User = Depends(get_current_user)):
    positions = await execution_nexus.get_positions(user_id=current_user.id, broker=broker)
    return positions

@router.get("/{symbol}", response_model=Position)
async def get_position(symbol: str, current_user: User = Depends(get_current_user)):
    position = await execution_nexus.get_position(user_id=current_user.id, symbol=symbol)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

@router.post("/{symbol}/close")
async def close_position(symbol: str, quantity: Optional[float] = None, current_user: User = Depends(get_current_user)):
    try:
        result = await execution_nexus.close_position(user_id=current_user.id, symbol=symbol, quantity=quantity)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
