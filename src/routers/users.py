from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.sql.annotation import Annotated
from sqlalchemy.sql.coercions import expect
from typing_extensions import Any
from src.validation import *
from src.database import *
from passlib.hash import pbkdf2_sha256 # type: ignore
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/")
async def create_user(user: UserCreate):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        repeat_user = session.scalars(select(User).where(User.username == db_user.username)).first()
        
        if repeat_user is not None:
            raise HTTPException(status_code= 400, detail= "The username already exists")

        db_user.password = pbkdf2_sha256.hash(user.password) #password hash
        
        session.add(db_user) #Resisters an intention to insert or modify
        session.commit() #Sends and commits all pending operations(inserts, updates, deletes) to the database
        session.refresh(db_user) #Synchronizes the obejct with the latest state of the data base
    return user
    
KEY = "kfladckmdfniewpeofmjncdvkslsdfkasdgnsdfs"

@router.post("/login")
async def user_login(user: UserCreate):
    with Session(engine) as session:
        username_exists = session.scalars(select(User).where(User.username == user.username)).first()
        if username_exists is None:
            raise HTTPException(status_code= 400, detail= "Username not found!")

        if not pbkdf2_sha256.verify(user.password, username_exists.password):
            raise HTTPException(status_code = 401, detail= "Invalid password")

        payload = {
            "sub": user.username,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        
        token = jwt.encode(payload, KEY, algorithm = "HS256")

        return token
        
security = HTTPBearer()
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials #select just the token

    try:
        payload = jwt.decode(token, KEY, algorithms=["HS256"])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code = 401, detail= "Invalid token")
    except Exception:
            raise HTTPException(status_code=401, detail="Token expirado ou inválido")

    with Session(engine) as session:
        db_user = session.scalars(select(User).where(User.username == username)).first()
        if db_user is None:
            raise HTTPException(status_code= 400, detail= "Username not found!")

        return db_user
        
dependency = Annotated[Any, Depends(user_login)] # login dependency to execute tasks actions

@router.post("/tasks")
async def create_task(task: TaskBase, commons: User = Depends(get_user)):
    with Session(engine) as session:
       db_task = Task.model_validate(task, update= {"user_id": commons.id})

       session.add(db_task)
       session.commit()
       session.refresh(db_task)

       return db_task

@router.get("/tasks")  
async def show_tasks(current: User = Depends(get_user)):
    with Session(engine) as session:
        tasks = session.scalars(select(Task).where(Task.user_id == current.id)).all()
        return tasks

@router.delete("/tasks/{tasks_id}")
async def delete_task(tasks_id: int, current: User = Depends(get_user)):
    with Session(engine) as session:
        current_tasks = session.scalars(select(Task).where(Task.user_id == current.id, Task.id == tasks_id)).first()

        if current_tasks is None:
            raise HTTPException(status_code= 404, detail= "Task not found!")

        session.delete(current_tasks)
        session.commit()