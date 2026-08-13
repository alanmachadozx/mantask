from sqlite3.dbapi2 import connect
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select

class User(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key=True)
    username: str
    password: str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread" : False}
engine =  create_engine(sqlite_url, echo = True, connect_args = connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    
@app.post("/user/")
async def create_user(user: User):
    with Session(engine) as session:
        session.add(user) #Resisters an intention to insert or modify
        session.commit() #Sends and commits all pending operations(inserts, updates, deletes) to the database
        session.refresh(user) #Synchronizes the obejct with the latest state of the data base
    return user