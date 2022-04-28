from sqlalchemy import Boolean, Column, Integer, String

from db.database import Base


class TodosModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

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
