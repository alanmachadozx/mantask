from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.sql.annotation import Annotated
from src.validation import *
from src.database import *
from passlib.hash import pbkdf2_sha256 # type: ignore
from datetime import datetime, timedelta
import jwt

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/")
async def create_user(user: UserCreate):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        repeat_user = session.scalars(select(User).where(User.username == db_user.username)).first()
        
        if repeat_user is not None:
            raise HTTPException(status_code= 400, detail= "The username already exists")

        db_user.password = pbkdf2_sha256.hash(user.password)
        
        session.add(db_user) #Resisters an intention to insert or modify
        session.commit() #Sends and commits all pending operations(inserts, updates, deletes) to the database
        session.refresh(db_user) #Synchronizes the obejct with the latest state of the data base
    return user

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
        key = "kfladckmdfniewpeofmjncdvkslsdfkasdgnsdfs"
        token = jwt.encode(payload, key, algorithm = "HS256")

        return token

dependency = Annotated[dict, Depends(user_login)]
