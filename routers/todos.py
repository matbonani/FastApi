from fastapi import Depends, HTTPException, status as http_status, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import models
from db.database import engine, get_db
from schemas.todos import CreateTodo
from routers.auth import get_current_user


router = APIRouter(prefix="/todos", tags=["todos"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


@router.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/", status_code=http_status.HTTP_200_OK)
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.TodosModel).all()


@router.get("/user")
async def todos_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.TodosModel).filter(models.TodosModel.owner_id == user.get("id")).all()


@router.get("/{todo_id}", status_code=http_status.HTTP_200_OK)
async def read_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model = db.query(models.TodosModel).filter(models.TodosModel.id == todo_id)\
        .filter(models.TodosModel.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo_model


@router.post("/", status_code=http_status.HTTP_201_CREATED)
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


@router.put("/{todo_id}", status_code=http_status.HTTP_200_OK)
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


@router.delete("/{todo_id}", status_code=http_status.HTTP_200_OK)
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
