from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.core.database import Base

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    layout = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    async def create(cls, db: AsyncSession, user_id: int, name: str, layout: dict):
        workspace_id = f"WS-{datetime.utcnow().timestamp()}"
        workspace = cls(id=workspace_id, user_id=user_id, name=name, layout=layout)
        db.add(workspace)
        await db.commit()
        await db.refresh(workspace)
        return workspace
    
    @classmethod
    async def get_by_user(cls, db: AsyncSession, user_id: int):
        result = await db.execute(select(cls).where(cls.user_id == user_id))
        return result.scalars().all()
    
    @classmethod
    async def get_by_id(cls, db: AsyncSession, workspace_id: str):
        result = await db.execute(select(cls).where(cls.id == workspace_id))
        return result.scalar_one_or_none()
    
    @classmethod
    async def update(cls, db: AsyncSession, workspace_id: str, user_id: int, name: str, layout: dict):
        result = await db.execute(select(cls).where(cls.id == workspace_id, cls.user_id == user_id))
        workspace = result.scalar_one_or_none()
        
        if workspace:
            workspace.name = name
            workspace.layout = layout
            workspace.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(workspace)
        
        return workspace
    
    @classmethod
    async def delete(cls, db: AsyncSession, workspace_id: str, user_id: int):
        result = await db.execute(select(cls).where(cls.id == workspace_id, cls.user_id == user_id))
        workspace = result.scalar_one_or_none()
        
        if workspace:
            await db.delete(workspace)
            await db.commit()
