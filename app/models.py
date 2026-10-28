from enum import Enum
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime


class TaskStatus(str, Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = None
    category: str = Field(index=True)
    task_date: datetime


class Task(TaskBase, table=True):
    task_id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.NEW)
    created_at: datetime = Field(default_factory=datetime.now)


class TaskPublic(TaskBase):
    task_id: UUID
    status: TaskStatus
    created_at: datetime


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    task_date: datetime | None = None
    status: TaskStatus | None = None