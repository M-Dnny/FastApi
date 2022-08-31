import uuid
from fastapi import FastAPI, File, Request, Depends, UploadFile

from app import schema

from . import models
from .database import engine, get_db
from .routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlalchemy.orm import session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.exception_handler(TypeError)
async def value_error_exception_handler(request: Request, exc: TypeError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

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
    return {"data": "Fuck Society"}


@app.post("/uploadimage")
async def upload_image(upload=schema.profile, image: UploadFile = File(...), db: session = Depends(get_db)):

    upload_img = models.Profile()
    # db.add(upload_img)
    # db.commit()
    # db.refresh(upload_img)

    image.filename = f"{uuid.uuid4()}.jpg"
    contents = await image.read()  # <-- Important!

    # example of how you can save the file
    dir = "./"
    with open(f"{dir}{image.filename}", "rb") as f:
        f.write(contents)

    return {"file": contents}
