from fastapi import FastAPI, Depends, HTTPException, status as http_status
from sqlalchemy.orm import Session


from db import models
from db.database import engine, get_db
from schemas.todos import CreateTodo
from auth import get_current_user


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/", status_code=http_status.HTTP_200_OK)
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.TodosModel).all()


@app.get("/todos/user")
async def todos_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.TodosModel).filter(models.TodosModel.owner_id == user.get("id")).all()


@app.get("/todo/{todo_id}", status_code=http_status.HTTP_200_OK)
async def read_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model = db.query(models.TodosModel).filter(models.TodosModel.id == todo_id)\
        .filter(models.TodosModel.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo_model


@app.post("/", status_code=http_status.HTTP_201_CREATED)
async def create_todo(todo: CreateTodo, user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    todo = todo.__dict__
    todo = models.TodosModel(**todo)
    todo.owner_id = user.get("id")
    db.add(todo)
    db.commit()
    return todo.serializer()


@app.put("/todo/{todo_id}", status_code=http_status.HTTP_200_OK)
async def update_todo(todo_id: int, todo: CreateTodo, user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    todo_model = db.query(models.TodosModel).filter(models.TodosModel.id == todo_id)\
        .filter(models.TodosModel.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()
    return todo_model.serializer()


@app.delete("/todo/{todo_id}", status_code=http_status.HTTP_200_OK)
async def read_todo(todo_id: int, user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model = db.query(models.TodosModel).filter(models.TodosModel.id == todo_id)\
        .filter(models.TodosModel.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
    return {"message": "Todo has been deleted"}
