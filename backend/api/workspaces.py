from typing import List

from fastapi import APIRouter, Depends, HTTPException
from backend.core.security import get_current_user
from backend.models.user import User
from backend.models.workspace import Workspace
from backend.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from backend.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/", response_model=WorkspaceResponse, status_code=201)
async def create_workspace(workspace: WorkspaceCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    created = await Workspace.create(db, user_id=current_user.id, name=workspace.name, layout=workspace.layout)
    return created

@router.get("/", response_model=List[WorkspaceResponse])
async def get_workspaces(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    workspaces = await Workspace.get_by_user(db, user_id=current_user.id)
    return workspaces

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    workspace = await Workspace.get_by_id(db, workspace_id)
    if not workspace or workspace.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(workspace_id: str, workspace: WorkspaceCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    updated = await Workspace.update(db, workspace_id=workspace_id, user_id=current_user.id, name=workspace.name, layout=workspace.layout)
    if not updated:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return updated

@router.delete("/{workspace_id}")
async def delete_workspace(workspace_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await Workspace.delete(db, workspace_id=workspace_id, user_id=current_user.id)
    return {"status": "deleted"}
