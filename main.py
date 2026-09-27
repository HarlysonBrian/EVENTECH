from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import date
from api import router


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="EVENTECH",
    description="Sistema de Gerenciamento de Eventos Acadêmicos",
    version="1.0.0"
)
app.include_router(router)

