from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class TodosModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UsersModel", back_populates="todos")

    def __init__(self, title: str, description: str, priority: int, complete: bool):
        self.title = title
        self.description = description
        self.priority = priority
        self.complete = complete

    def serializer(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "complete": self.complete
        }


class UsersModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("TodosModel", back_populates="owner")

    def __init__(self, email: str, username: str, first_name: str, last_name: str, password: str):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def serializer(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active
        }
