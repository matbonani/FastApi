from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
