from fastapi import FastAPI
from src.database import *
from src.routers.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    
