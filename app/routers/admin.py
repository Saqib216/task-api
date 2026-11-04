from sqlmodel import select
from typing import Annotated
from uuid import UUID
from app.models import TaskPublic, Task, TaskAdminCreate, User, TaskUpdate
from app.dependencies import require_admin, SessionDep, TaskPlainDep
from fastapi import APIRouter, Depends, status, Query, HTTPException

router = APIRouter(
    prefix="/admin/tasks", tags=["admin"], dependencies=[Depends(require_admin)]
)


@router.get("", response_model=list[TaskPublic])
def get_all_tasks(
    session: SessionDep,
    user_id: UUID | None = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    query = select(Task)
    if user_id:
        query = query.where(Task.user_id == user_id)

    tasks = session.exec(query.offset(offset).limit(limit)).all()
    return tasks


@router.post("", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task_for_user(task_in: TaskAdminCreate, session: SessionDep):
    target_user = session.get(User, task_in.user_id)
    if not target_user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {task_in.user_id} not found",
        )

    db_task = Task.model_validate(task_in)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task_admin(task: TaskPlainDep, task_update: TaskUpdate, session: SessionDep):
    update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_admin(task: TaskPlainDep, session: SessionDep):
    session.delete(task)
    session.commit()
