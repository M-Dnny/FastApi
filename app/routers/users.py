
from os import getcwd
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Request, Response, HTTPException, File, UploadFile, BackgroundTasks
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.orm import session

from app import oauth

from ..database import get_db
from ..import utils,  models, schema

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from PIL import Image
import base64
from threading import Timer


app = FastAPI()

# RESIZE IMAGES FOR DIFFERENT DEVICES


def resize_image(filename: str):
    sizes = [{
        "width": 1280,
        "height": 720
    }]

    for size in sizes:
        size_defined = size['width'], size['height']

        image = Image.open(PATH_FILES + filename, mode="r")
        image.thumbnail(size_defined)
        image.save(PATH_FILES + str(size['height']) + "_" + filename)
    print("success")


@app.exception_handler(TypeError)
async def value_error_exception_handler(request: Request, exc: TypeError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
# Create User

routers = APIRouter(
    prefix="/user",
    tags={"Users"}
)

# Upload image

# PATH_FILES = getcwd() + "/"
PATH_FILES = "D:\Python\FastApi-Python\store\\"


@routers.post("/uploadimage")
async def upload_image(background_tasks: BackgroundTasks, upload=schema.profile, file: UploadFile = File(...), db: session = Depends(get_db)):
    image = PATH_FILES + file.filename
    image_name = PATH_FILES + f"720_{file.filename}"
    with open(image, 'wb+') as f:
        content = await file.read()
        upload_img = models.Profile(image_path=image_name)

        image_id = 1

        try:

            f.write(content)
            f.close()
            # db.add(upload_img)
            # db.commit()
            # db.refresh(upload_img)

            image_url = f"http://127.0.0.1:8000/user/getimage/?image_id={upload_img.id}"
            print(image_url)

            # upload_img = models.Profile(
            #     id=upload_img.id, image_name=image_name, image_url=image_url)

            # db.add(upload_img)
            # db.query('Profile').update({"null": image_url})

            image_id_temp = upload_img.id

            # db.query(models.Profile).filter(
            #     models.Profile.id == image_id_temp).update(
            #     {"image_url": image_url}, synchronize_session=False)
            # print("temp: ", temp)
            # db.commit()
            # db.refresh(upload_img)

            # db.refresh(upload_img)
            # print("print1:", db.query(models.Profile).update(
            #     {models.Profile.image_url: image_url}))

            # print("print 2: ", db.query(models.Profile).update(
            #     {"image_url": image_url}, synchronize_session=False))

            background_tasks.add_task(resize_image, filename=file.filename)

        except Exception as e:
            retVal = {'status': 'False',
                      'msg': 'Python3 Exception : {}'.format(e)}
        else:
            retVal = {'status': 'True', 'msg': 'download',
                      "data": upload_img}
        f.close()

        return {"file": retVal}

# get image


@routers.get("/getimage")
def get_image(image_id: int, db: session = Depends(get_db)):
    print("image_id")
    print(image_id)
    try:
        # image = db.query(models.Profile).filter(
        #     models.Profile.id == image_id).first()

        image = db.query(models.User).filter(
            models.User.id == image_id).first()

        image_path = image
        print("Image path")
        print(image_path.image_path)

        if not image:
            return {"message": "Image not found"}

        file = FileResponse(path=image_path.image_path)

        return file

    except Exception as e:
        return {'status': 'False',
                'msg': 'Exception : {}'.format(e)}


@routers.get('/getimages')
def getImages(db: session = Depends(get_db)):

    try:
        image = db.query(models.Profile).all()
        return image

    except Exception as e:
        print(e)


@routers.post("/register", status_code=status.HTTP_201_CREATED)
async def register(background_tasks: BackgroundTasks, user: schema.UserCreate = Depends(schema.UserCreate.as_form), db: session = Depends(get_db), profile_image: UploadFile = File(...),):

    image = PATH_FILES + profile_image.filename
    image_name = PATH_FILES + f"720_{profile_image.filename}"
    with open(image, 'wb') as f:
        content = await profile_image.read()

        f.write(content)
        f.close()

        print("image name:", profile_image.filename)
        print('id:', models.User.id)

    try:
        # Check mail

        mailCheck = db.query(models.User).filter(
            models.User.email == user.email).first()

        # check phone number

        numberCheck = db.query(models.User).filter(
            models.User.phone_number == user.phone_number).first()

        if mailCheck:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"{models.User.email.key} must be unique"
            )
        if numberCheck:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"{models.User.phone_number.key} must be unique"
            )

        hased_password = utils.hash(user.password)

        user.password = hased_password

        new_user = models.User(**user.dict(), image_path=image_name)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        image_url = f"http://127.0.0.1:8000/user/getimage/?image_id={new_user.id}"

        image_id_temp = new_user.id

        temp = db.query(models.User).filter(
            models.User.id == image_id_temp).update(
            {"image_url": image_url}, synchronize_session=False)
        print(temp)

        db.commit()
        db.refresh(new_user)
        background_tasks.add_task(
            resize_image, filename=profile_image.filename)

        return {"message": "Registered Successfull", "status": "True"}
    except ValidationError as e:
        return {"dssd"}


@routers.get('/{id}', response_model=schema.UserOut)
async def getUserInfo(id: int, db: session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user does not exist")

    return user
