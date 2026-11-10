from fastapi.params import Body
from fastapi import FastAPI

app = FastAPI()


# Route 1: Root URL
@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


# Route 2: Posts URL
@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createpost")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return{"message":"succesfully created posts"}