from fastapi import APIRouter
from src.validation import *
from src.database import *

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/")
async def create_user(user: User):
    with Session(engine) as session:
        session.add(user) #Resisters an intention to insert or modify
        session.commit() #Sends and commits all pending operations(inserts, updates, deletes) to the database
        session.refresh(user) #Synchronizes the obejct with the latest state of the data base
    return user

@router.get("/")
async def read_user():
    with Session(engine) as session:
        user = session.exec(select(User)).all() 
        return user