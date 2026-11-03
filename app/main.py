from app.routers import tasks, auth
from fastapi import FastAPI
from .database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(
    tasks.router
)

app.include_router(auth.router)