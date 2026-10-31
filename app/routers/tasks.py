from uuid import UUID
from sqlmodel import select
from typing import Annotated
from app.models import Task, TaskCreate, TaskPublic, TaskUpdate
from app.database import SessionDep
from fastapi import APIRouter, status, Query, HTTPException, Depends

def get_task_or_404(session: SessionDep, task_id: UUID)->Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

TaskDep = Annotated[Task, Depends(get_task_or_404)]

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: SessionDep):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("", response_model=list[TaskPublic])
def get_tasks(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskPublic)
def get_task(task: TaskDep):
    return task


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(task: TaskDep, task_update: TaskUpdate, session: SessionDep):
    update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task: TaskDep, session: SessionDep):
    session.delete(task)
    session.commit()