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

def find_index_post(id):
    for i , p in enumerate(my_post):
        if p['id'] == id :
            return i


# Route 1: Root URL
@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


# Route 2: Posts URL
@app.get("/posts")
def get_posts():
    return {"data": my_post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
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

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} dose not exist")

    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} dose not exist")

    post_dict = post.dict()             
    post_dict['id'] = id 
    my_post[index] = post_dict         
    return {"data": post_dict}

