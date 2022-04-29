from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import models
from db.database import engine, get_db
from routers.auth import get_current_user, verify_password, get_password_hash
from schemas.users import UserVerification, CreateUser

router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)


@router.post("/create/user")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user = user.__dict__
    user_model = models.UsersModel(**user)
    user_model.password = get_password_hash(user["password"])

    db.add(user_model)
    db.commit()
    return user_model.serializer()


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.UsersModel).all()


@router.get("/user/{user_id}")
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.UsersModel).filter(models.UsersModel.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_model


@router.get("/user/")
async def user_by_query(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.UsersModel).filter(models.UsersModel.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_model


@router.put("/password")
async def password_change(user_verification: UserVerification, user: dict = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model = db.query(models.UsersModel).filter(models.UsersModel.id == user.get("id")).first()
    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(
                user_verification.password, user_model.password):
            user_model.password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return {"message": "Password changed"}
    return {"message": "Password is Invalid"}


@router.delete("/user")
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model = db.query(models.UsersModel).filter(models.UsersModel.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_model)
    db.commit()
    return {"message": "User succsfully deleted "}
