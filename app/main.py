import base64
from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}   

@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    
    if not query.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    
    if not query.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": query.first()}

