from app.dependencies import CurrentUser
from app.models import UserPublic
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserPublic)
def get_user(current_user: CurrentUser):
    return current_user