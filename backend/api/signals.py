from typing import List

from fastapi import APIRouter, Depends
from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.ai_agents import SignalGenerator
from backend.schemas.signal import Signal, SignalCreate

router = APIRouter()
signal_generator = SignalGenerator()

@router.get("/", response_model=List[Signal])
async def get_signals(symbol: str = None, current_user: User = Depends(get_current_user)):
    signals = await signal_generator.get_signals(user_id=current_user.id, symbol=symbol)
    return signals

@router.post("/", response_model=Signal, status_code=201)
async def create_signal(signal: SignalCreate, current_user: User = Depends(get_current_user)):
    created_signal = await signal_generator.create_signal(user_id=current_user.id, signal=signal)
    return created_signal

@router.get("/live")
async def get_live_signals(current_user: User = Depends(get_current_user)):
    signals = await signal_generator.scan_live_signals(user_id=current_user.id)
    return signals
