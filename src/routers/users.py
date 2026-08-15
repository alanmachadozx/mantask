from fastapi import APIRouter
from fastapi import HTTPException
from src.validation import *
from src.database import *
from passlib.hash import pbkdf2_sha256 # type: ignore

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