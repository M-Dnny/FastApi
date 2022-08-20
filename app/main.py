from fastapi import FastAPI

from . import models
from .database import engine
from .routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.routers)
app.include_router(posts.routers)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def get():
    return {"data":"Fuck Society"}
