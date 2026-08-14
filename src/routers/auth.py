from main import *

@app.post("/user/")
async def create_user(user: User):
    with Session(database.engine) as session:
        session.add(user) #Resisters an intention to insert or modify
        session.commit() #Sends and commits all pending operations(inserts, updates, deletes) to the database
        session.refresh(user) #Synchronizes the obejct with the latest state of the data base
    return user

@app.get("/user/")
async def read_user():
    with Session(database.engine) as session:
        user = session.exec(select(User)).all() 
        return user