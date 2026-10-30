from uuid import UUID
from sqlmodel import select
from typing import Annotated
from app.models import Task, TaskCreate, TaskPublic, TaskUpdate
from app.database import SessionDep
from fastapi import APIRouter, status, Query, HTTPException

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post("", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate, session: SessionDep):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("", response_model=list[TaskPublic])
def get_tasks(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskPublic)
def get_task(task_id: UUID, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(task_id: UUID, task:TaskUpdate, session: SessionDep):
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(task_data)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, session: SessionDep):
    task = session.get(Task, task_id)
    if not task: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    session.delete(task)
    session.commit()