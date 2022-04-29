from fastapi import FastAPI

from company import companyapis
from routers import auth, todos
from db import models
from db.database import engine

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)


models.Base.metadata.create_all(bind=engine)

