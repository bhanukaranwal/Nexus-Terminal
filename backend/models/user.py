from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    wallet_address = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: int):
        result = await db.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()
    
    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str):
        result = await db.execute(select(cls).where(cls.email == email))
        return result.scalar_one_or_none()
    
    @classmethod
    async def create(cls, db: AsyncSession, email: str, username: str, hashed_password: str):
        user = cls(email=email, username=username, hashed_password=hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @classmethod
    async def get_or_create_by_wallet(cls, db: AsyncSession, wallet_address: str):
        result = await db.execute(select(cls).where(cls.wallet_address == wallet_address))
        user = result.scalar_one_or_none()
        
        if not user:
            user = cls(
                email=f"{wallet_address[:8]}@nexus.trading",
                username=wallet_address[:12],
                wallet_address=wallet_address
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        return user
