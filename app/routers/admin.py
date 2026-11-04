from app.dependencies import require_admin
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/admin/tasks",
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)

