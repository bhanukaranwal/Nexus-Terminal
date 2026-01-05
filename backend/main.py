from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import structlog

from backend.core.config import settings
from backend.core.database import init_db
from backend.core.events import startup_event, shutdown_event
from backend.api import auth, data, orders, positions, portfolio, signals, strategies, scanners, workspaces, blockchain, defi, quantum
from backend.services.data_oracle import DataOracle
from backend.core.telemetry import setup_telemetry

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await startup_event()
    await init_db()
    setup_telemetry()
    logger.info("nexus_startup", version=settings.VERSION)
    yield
    await shutdown_event()
    logger.info("nexus_shutdown")

app = FastAPI(
    title="Nexus Trading Terminal API",
    description="The Ultimate Futuristic Trading Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(data.router, prefix="/api/data", tags=["Market Data"])
app.include_router(orders.router, prefix="/api/orders", tags=["Order Management"])
app.include_router(positions.router, prefix="/api/positions", tags=["Positions"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(signals.router, prefix="/api/signals", tags=["Trading Signals"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["Strategies"])
app.include_router(scanners.router, prefix="/api/scanners", tags=["Market Scanners"])
app.include_router(workspaces.router, prefix="/api/workspaces", tags=["Workspaces"])
app.include_router(blockchain.router, prefix="/api/blockchain", tags=["Blockchain"])
app.include_router(defi.router, prefix="/api/defi", tags=["DeFi"])
app.include_router(quantum.router, prefix="/api/quantum", tags=["Quantum Optimization"])

data_oracle = DataOracle()

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy", "service": "nexus-terminal"})

@app.websocket("/ws/market/{symbol}")
async def websocket_market_data(websocket: WebSocket, symbol: str):
    await websocket.accept()
    subscription_id = await data_oracle.subscribe(symbol, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await data_oracle.unsubscribe(subscription_id)
        logger.info("websocket_disconnect", symbol=symbol)

@app.websocket("/ws/orderflow/{symbol}")
async def websocket_orderflow(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        async for message in data_oracle.stream_orderflow(symbol):
            await websocket.send_json(message)
    except WebSocketDisconnect:
        logger.info("orderflow_disconnect", symbol=symbol)

@app.websocket("/ws/agents")
async def websocket_agents(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            logger.info("agent_command", command=data)
            await websocket.send_json({"status": "acknowledged"})
    except WebSocketDisconnect:
        logger.info("agent_disconnect")

@app.get("/")
async def root():
    return {
        "message": "Welcome to NEXUS - The Ultimate Futuristic Trading Terminal",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
