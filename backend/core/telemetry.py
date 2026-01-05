from prometheus_client import Counter, Histogram, Gauge
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

orders_total = Counter('nexus_orders_total', 'Total orders placed', ['broker', 'status'])
execution_time = Histogram('nexus_execution_seconds', 'Order execution time', ['broker'])
active_websockets = Gauge('nexus_active_websockets', 'Active WebSocket connections')
ai_predictions = Counter('nexus_ai_predictions_total', 'AI predictions made', ['model'])
backtest_duration = Histogram('nexus_backtest_seconds', 'Backtest execution time')

def setup_telemetry():
    logger = structlog.get_logger()
    logger.info("telemetry_initialized")
