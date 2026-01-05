import asyncio
import structlog
from backend.services.data_oracle import DataOracle
from backend.services.ai_agents import AgentOrchestrator

logger = structlog.get_logger()

data_oracle: DataOracle = None
agent_orchestrator: AgentOrchestrator = None

async def startup_event():
    global data_oracle, agent_orchestrator
    
    logger.info("initializing_data_oracle")
    data_oracle = DataOracle()
    await data_oracle.initialize()
    
    logger.info("initializing_agent_orchestrator")
    agent_orchestrator = AgentOrchestrator()
    await agent_orchestrator.start()
    
    logger.info("nexus_ready")

async def shutdown_event():
    global data_oracle, agent_orchestrator
    
    logger.info("shutting_down_nexus")
    
    if data_oracle:
        await data_oracle.shutdown()
    
    if agent_orchestrator:
        await agent_orchestrator.stop()
    
    logger.info("nexus_shutdown_complete")
