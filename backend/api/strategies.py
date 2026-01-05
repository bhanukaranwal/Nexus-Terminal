from typing import List

from fastapi import APIRouter, Depends, HTTPException
from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.backtester_quantum import QuantumBacktester
from backend.schemas.strategy import Strategy, StrategyCreate, BacktestResult

router = APIRouter()
backtester = QuantumBacktester()

@router.post("/", response_model=Strategy, status_code=201)
async def create_strategy(strategy: StrategyCreate, current_user: User = Depends(get_current_user)):
    created = await backtester.create_strategy(user_id=current_user.id, strategy=strategy)
    return created

@router.get("/", response_model=List[Strategy])
async def get_strategies(current_user: User = Depends(get_current_user)):
    strategies = await backtester.get_strategies(user_id=current_user.id)
    return strategies

@router.post("/{strategy_id}/backtest", response_model=BacktestResult)
async def backtest_strategy(strategy_id: str, current_user: User = Depends(get_current_user)):
    result = await backtester.run_backtest(strategy_id=strategy_id, user_id=current_user.id)
    return result

@router.post("/{strategy_id}/optimize")
async def optimize_strategy(strategy_id: str, current_user: User = Depends(get_current_user)):
    result = await backtester.quantum_optimize(strategy_id=strategy_id, user_id=current_user.id)
    return result

@router.post("/{strategy_id}/deploy")
async def deploy_strategy(strategy_id: str, current_user: User = Depends(get_current_user)):
    try:
        deployment = await backtester.deploy_live(strategy_id=strategy_id, user_id=current_user.id)
        return deployment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
