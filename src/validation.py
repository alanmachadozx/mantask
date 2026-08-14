
from pydantic import BaseModel, AfterValidator, ValidationError
from sqlmodel import Field, SQLModel, Session, create_engine, select

class User(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key=True)
    username: str = Field(min_length = 5)
    password: str = Field(min_length = 8)   