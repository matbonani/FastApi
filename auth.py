from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext

from db import models


class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()


def get_password_hash(password):
    return bcrypt_context.hash(password)


@app.post("/create/user")
async def create_user(user: CreateUser):
    user_model = models.UsersModel()
    user_model.email = user.email
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name

    has_password = get_password_hash(user.password)
    user_model.hashed_password = has_password
    return user_model
