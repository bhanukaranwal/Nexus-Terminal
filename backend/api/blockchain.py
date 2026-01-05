from fastapi import APIRouter, Depends
from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.token_engine import TokenEngine

router = APIRouter()
token_engine = TokenEngine()

@router.post("/wallet/connect")
async def connect_wallet(wallet_address: str, chain: str = "ethereum", current_user: User = Depends(get_current_user)):
    result = await token_engine.connect_wallet(user_id=current_user.id, wallet_address=wallet_address, chain=chain)
    return result

@router.get("/wallet/balance")
async def get_wallet_balance(chain: str = "ethereum", current_user: User = Depends(get_current_user)):
    balance = await token_engine.get_balance(user_id=current_user.id, chain=chain)
    return balance

@router.post("/token/mint")
async def mint_token(name: str, symbol: str, supply: int, current_user: User = Depends(get_current_user)):
    result = await token_engine.mint_token(user_id=current_user.id, name=name, symbol=symbol, supply=supply)
    return result

@router.get("/transactions")
async def get_transactions(chain: str = "ethereum", current_user: User = Depends(get_current_user)):
    txs = await token_engine.get_transactions(user_id=current_user.id, chain=chain)
    return txs
