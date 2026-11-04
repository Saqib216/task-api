from app.models import Task
from app.database import engine
from app.security import decode_access_token
from jwt.exceptions import InvalidTokenError
from uuid import UUID
from app.models import User, Role
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlmodel import Session

# session dependency


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = decode_access_token(token)
        sub: str | None = decoded_token.get("sub")

        if sub is None:
            raise credentials_exception
        user_id = UUID(sub)

        current_user = session.get(User, user_id)
        if not current_user:
            raise credentials_exception
        return current_user

    except (InvalidTokenError, ValueError):
        raise credentials_exception


CurrentUser = Annotated[User, Depends(get_current_user)]


# Admin Verification Dependency
def require_admin(current_user: CurrentUser) -> User:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return current_user


AdminDep = Annotated[User, Depends(require_admin)]


# plain task loader (just checks ID) - for ADMIN
def get_task_by_id(task_id: UUID, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


TaskPlainDep = Annotated[Task, Depends(get_task_by_id)]


# Ownership task loader (Depends in another Depends) - for EMPLOYEE
def get_task_with_ownership(task: TaskPlainDep, current_user: CurrentUser) -> Task:
    if task.user_id != current_user.user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


TaskDep = Annotated[Task, Depends(get_task_with_ownership)]
