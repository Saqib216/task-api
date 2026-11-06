from sqlmodel import select
from typing import Annotated
from app.models import Task, TaskPublic, TaskStatusUpdate
from app.dependencies import SessionDep, CurrentUser, TaskDep
from fastapi import APIRouter, status, Query, HTTPException
from ..task_transitions import ALLOWED_TRANSITIONS

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("", response_model=list[TaskPublic])
def get_tasks(
    session: SessionDep,
    current_user: CurrentUser,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    tasks = session.exec(
        select(Task)
        .where(Task.user_id == current_user.user_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return tasks


@router.get("/{task_id}", response_model=TaskPublic)
def get_task(task: TaskDep):
    return task


@router.patch("/{task_id}/status", response_model=TaskPublic)
def task_status_update(
    task: TaskDep, new_status: TaskStatusUpdate, session: SessionDep
):
    if new_status.status not in ALLOWED_TRANSITIONS.get(task.status, []):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Cannot move task from {task.status.value} to {new_status.status.value}",
        )

    task.status = new_status.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task