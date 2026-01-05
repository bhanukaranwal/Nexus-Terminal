from typing import List

from fastapi import APIRouter, Depends
from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.execution_nexus import ExecutionNexus
from backend.schemas.portfolio import PortfolioSummary, PerformanceMetrics

router = APIRouter()
execution_nexus = ExecutionNexus()

@router.get("/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(current_user: User = Depends(get_current_user)):
    summary = await execution_nexus.get_portfolio_summary(user_id=current_user.id)
    return summary

@router.get("/performance", response_model=PerformanceMetrics)
async def get_performance_metrics(period: str = "1M", current_user: User = Depends(get_current_user)):
    metrics = await execution_nexus.calculate_performance_metrics(user_id=current_user.id, period=period)
    return metrics

@router.get("/allocation")
async def get_allocation(current_user: User = Depends(get_current_user)):
    allocation = await execution_nexus.get_asset_allocation(user_id=current_user.id)
    return allocation

@router.get("/pnl")
async def get_pnl_history(period: str = "1Y", current_user: User = Depends(get_current_user)):
    pnl = await execution_nexus.get_pnl_history(user_id=current_user.id, period=period)
    return pnl
