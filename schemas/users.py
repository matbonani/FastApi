from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
