from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


from db import models
from db.database import engine, get_db
from schemas.todos import CreateTodo

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.TodosModel).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.TodosModel).filter(models.TodosModel.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo_model.serializer()


@app.post("/")
async def create_todo(todo: CreateTodo, db: Session = Depends(get_db)):
    todo = todo.__dict__
    todo = models.TodosModel(**todo)
    db.add(todo)
    db.commit()
    return todo.serializer()


@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: CreateTodo, db: Session = Depends(get_db)):
    todo_model = db.query(models.TodosModel).filter(models.TodosModel.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()
    return todo_model.serializer()


@app.delete("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.TodosModel).filter(models.TodosModel.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
    return {"message": "Todo has been deleted"}
