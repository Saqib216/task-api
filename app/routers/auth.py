from datetime import timedelta
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from app.security import (
    hash_password,
    DUMMY_HASH,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.dependencies import SessionDep
from sqlmodel import select, func
from fastapi import status, HTTPException, APIRouter, Depends
from app.models import UserCreate, UserPublic, User, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate, session: SessionDep):
    existing_user = session.exec(
        select(User.email).where(User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Email already exists")

    hashed_password = hash_password(user.password)
    db_user = User.model_validate(user, update={"hashed_password": hashed_password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    user = session.exec(
        select(User).where(func.lower(User.email) == form_data.username.lower())
    ).first()

    if not user:
        verify_password(form_data.password, DUMMY_HASH)
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

