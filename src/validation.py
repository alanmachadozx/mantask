from datetime import date

from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=6)

#this model will sent to the database
class User(UserBase, table=True):
    id: int | None = Field(default = None, primary_key = True)

class UserCreate(UserBase):
    pass

class TaskBase(SQLModel):
    title: str
    description: str
    limit_date: date | None = None

class Task(TaskBase, table = True):
    id: int | None = Field(default = None, primary_key= True)
    user_id: int = Field(foreign_key= "user.id")