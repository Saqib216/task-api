# 1. get SECRET_KEY & ALGORITHM from .env
from typing import Annotated
from datetime import datetime, timedelta, timezone
import os
import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 2. Password Hashing Tool (Argon2)
password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# 3. JWT Token Generator Tool
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # copy original data so that original data may not get changed during modification:
    to_encode = data.copy()

    # Calculate Expiry Time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Put expiry('exp') in Payload
    to_encode.update({"exp": expire})

    # Encode the token by signing it with secret_key digitally:
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# utility function to decode the jwt token:
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
