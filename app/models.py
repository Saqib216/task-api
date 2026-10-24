from pydantic import Field
from sqlmodel import SQLModel

class Task(SQLModel, table=True):
    task_id: int | None = Field(default=None, primary_key=True)
    