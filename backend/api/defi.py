from fastapi import APIRouter, Depends, HTTPException
from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.defi_bridge import DeFiBridge

router = APIRouter()
defi_bridge = DeFiBridge()

@router.post("/lend")
async def lend_assets(protocol: str, asset: str, amount: float, current_user: User = Depends(get_current_user)):
    try:
        result = await defi_bridge.lend(user_id=current_user.id, protocol=protocol, asset=asset, amount=amount)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/borrow")
async def borrow_assets(protocol: str, asset: str, amount: float, collateral: str, current_user: User = Depends(get_current_user)):
    try:
        result = await defi_bridge.borrow(user_id=current_user.id, protocol=protocol, asset=asset, amount=amount, collateral=collateral)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/swap")
async def swap_tokens(from_token: str, to_token: str, amount: float, slippage: float = 0.5, current_user: User = Depends(get_current_user)):
    try:
        result = await defi_bridge.swap(user_id=current_user.id, from_token=from_token, to_token=to_token, amount=amount, slippage=slippage)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/apy")
async def get_apy_rates(current_user: User = Depends(get_current_user)):
    rates = await defi_bridge.get_apy_rates()
    return rates

@router.post("/yield-farm")
async def start_yield_farming(protocol: str, pool: str, amount: float, current_user: User = Depends(get_current_user)):
    try:
        result = await defi_bridge.yield_farm(user_id=current_user.id, protocol=protocol, pool=pool, amount=amount)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
