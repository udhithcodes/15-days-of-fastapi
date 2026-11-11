from fastapi.openapi.utils import status_code_ranges
from typing import Optional
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str 
    publish : bool = True
    rating :Optional[int] = None

my_post = [{"title": "welcome to fastapi udhith", "content": "post 1", "id":1},
            {"title":"welcome raj", "content":"post 2", "id":2}]


def find_post(id):
    for p in my_post:
        if p["id"] == id :
            return p


# Route 1: Root URL
@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


# Route 2: Posts URL
@app.get("/posts")
def get_posts():
    return {"data": my_post}

@app.post("/posts")
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_post.append(post_dict)
    return{"data": post_dict}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    if not  post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id : {id} not found")
    return{"post_detials": post} 

