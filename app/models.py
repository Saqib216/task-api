from pydantic import EmailStr
from enum import Enum
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class TaskStatus(str, Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Role(str, Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"

class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = None
    category: str = Field(index=True)
    task_date: datetime


class Task(TaskBase, table=True):
    task_id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.NEW)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID = Field(foreign_key="user.user_id", index=True)


class TaskPublic(TaskBase):
    task_id: UUID
    status: TaskStatus
    created_at: datetime
    user_id: UUID


class TaskCreate(TaskBase):
    pass

class TaskAdminCreate(TaskCreate):
    user_id: UUID

class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    task_date: datetime | None = None
    status: TaskStatus | None = None


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)


class User(UserBase, table=True):
    user_id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    role: Role = Field(default=Role.EMPLOYEE)


class UserPublic(UserBase):
    user_id: UUID
    created_at: datetime
    role: Role


class UserCreate(UserBase):
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str
