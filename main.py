from fastapi import FastAPI

from db import models
from db.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def create_database():
    return {"message": "Created"}