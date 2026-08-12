from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.post("/user/")
async def create_user(user: User):
    return user