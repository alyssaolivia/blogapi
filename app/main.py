import base64
from random import randrange
import time
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from passlib.context import CryptContext
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post, auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
