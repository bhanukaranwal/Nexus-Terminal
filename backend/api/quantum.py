from fastapi import APIRouter, Depends
from backend.core.security import get_current_user
from backend.models.user import User
from backend.utils.quantum_opt import QuantumOptimizer

router = APIRouter()
quantum_optimizer = QuantumOptimizer()

@router.post("/optimize-portfolio")
async def optimize_portfolio(assets: list, returns: list, risk_tolerance: float, current_user: User = Depends(get_current_user)):
    result = await quantum_optimizer.optimize_portfolio(assets=assets, returns=returns, risk_tolerance=risk_tolerance)
    return result

@router.post("/optimize-strategy")
async def optimize_strategy_params(strategy_id: str, param_space: dict, current_user: User = Depends(get_current_user)):
    result = await quantum_optimizer.optimize_strategy(strategy_id=strategy_id, param_space=param_space)
    return result

@router.post("/predict-regime")
async def predict_market_regime(symbols: list, current_user: User = Depends(get_current_user)):
    result = await quantum_optimizer.predict_regime(symbols=symbols)
    return result
