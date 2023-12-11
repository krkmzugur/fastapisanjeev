from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth , vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello word"}










""" # Örnek olarak 10 elemanlı bir liste tanımlama (Pydantic modeli olmadan)
my_posts = [
    {"id": i, "title": f"Title {i}", "content": f"Content {i}"}
    for i in range(1, 11)
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i """



    