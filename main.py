from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import auth, todos, users
from db import models
from db.database import engine

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)

