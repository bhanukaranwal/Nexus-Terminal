from typing import List

from fastapi import APIRouter, Depends
from backend.core.security import get_current_user
from backend.models.user import User
from backend.services.ai_agents import MarketScanner
from backend.schemas.scanner import ScanResult, ScannerConfig

router = APIRouter()
scanner = MarketScanner()

@router.post("/run", response_model=List[ScanResult])
async def run_scanner(config: ScannerConfig, current_user: User = Depends(get_current_user)):
    results = await scanner.scan(config=config, user_id=current_user.id)
    return results

@router.get("/presets")
async def get_presets(current_user: User = Depends(get_current_user)):
    presets = await scanner.get_presets()
    return presets

@router.post("/unusual-options")
async def scan_unusual_options(current_user: User = Depends(get_current_user)):
    results = await scanner.scan_unusual_options()
    return results

@router.post("/orderflow-anomalies")
async def scan_orderflow_anomalies(current_user: User = Depends(get_current_user)):
    results = await scanner.scan_orderflow_anomalies()
    return results
