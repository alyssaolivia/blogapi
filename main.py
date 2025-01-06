from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "Post 1", "content": "This is a post", "published": True, "rating": 5, "id" : 1}, {"title": "Post 2", "content": "This is another post", "published": False, "rating": 4, "id" : 2}]

def fetch_posts(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post)
    post_dict = post.dict()
    post_dict["id"] = randrange(10000)
    my_posts.append(post_dict)
    return {"data": post_dict}   

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = fetch_posts(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = fetch_posts(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    my_posts.remove(post)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    old_post = fetch_posts(id)
    if not old_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_index = my_posts.index(old_post)
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    return {"data": post_dict}

