from app.security import hash_password
from app.database import SessionDep
from sqlmodel import select
from fastapi import status, HTTPException, APIRouter
from app.models import UserCreate, UserPublic, User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate, session: SessionDep):
    existing_user = session.exec(select(User.email).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Email already exists")

    hashed_password = hash_password(user.password)
    db_user = User.model_validate(user, update={"hashed_password": hashed_password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


