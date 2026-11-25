from pydantic_core.core_schema import counter_schema
from fastapi.openapi.utils import status_code_ranges
from typing import Optional
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str 
    published : bool = True

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="myapp", user="myuser",
        password="mysecretpassword", cursor_factory=RealDictCursor)
        curser = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database faild!")
        print("Error :", error)
        time.sleep(2)

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
    curser.execute("""SELECT * FROM posts """)
    posts = curser.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post : Post): 

    curser.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = curser.fetchone()
    conn.commit()
    return{"data": new_post}

@app.get("/posts/{id}") 
def get_post(id:int):
    curser.execute("""SELECT * FROM posts WHERE id = %s """, (str(id))) 
    post = curser.fetchone()

    if not  post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id : {id} not found")
    return{"post_detials": post} 

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    curser.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = curser.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} dose not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    curser.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                  (post.title, post.content, post.published, str(id)))
    updated_post = curser.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id : {id} dose not exist")
    
    return {"data": updated_post}

