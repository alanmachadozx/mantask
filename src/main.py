from fastapi import FastAPI
import database
from validation import *

app = FastAPI()
@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

    
