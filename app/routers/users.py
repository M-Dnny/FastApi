
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import session

from ..database import get_db

from ..import utils,  models, schema

# Create User

routers = APIRouter(
    prefix="/user",
    tags={"Users"}
)


@routers.post("/register", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def register(user: schema.UserCreate, db: session = Depends(get_db)):

    # hashing the pass

    # hased_password = pwd_contect.hash(user.password)
    hased_password = utils.hash(user.password)

    user.password = hased_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@routers.get('/{id}', response_model=schema.UserOut)
async def getUserInfo(id: int, db: session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user does not exist")

    return user
