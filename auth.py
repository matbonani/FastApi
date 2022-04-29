from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

from db.database import get_db, engine
from db import models
from schemas.users import CreateUser

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

oauth_bearer = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.UsersModel).filter(models.UsersModel.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_acces_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username and user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/create/user")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user = user.__dict__
    user_model = models.UsersModel(**user)
    user_model.password = get_password_hash(user["password"])

    db.add(user_model)
    db.commit()
    return user_model.serializer()


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_expire = timedelta(minutes=20)
    token = create_acces_token(user.username, user.id, expires_delta=token_expire)
    return {"token": token}

