from sqlmodel import select
from typing import Annotated
from app.models import Task, TaskCreate, TaskPublic
from app.database import SessionDep
from fastapi import APIRouter, status, Query

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post("/", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
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
