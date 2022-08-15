from base64 import decode
from email.policy import HTTP
import json
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app import models
from . import schema, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from .config import setting

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_min

# Create token


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # json_str = json.dumps({'expiration':expire}, default=str)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Verify Token


def verify_token(token: str, cred_exceptions):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get('user_id')

        if id is None:
            raise cred_exceptions

        token_data = schema.TokenData(id=id)

    except JWTError:
        raise cred_exceptions

    return token_data


# get current user

def get_current_user(token: str = Depends(oauth_scheme), db: session = Depends(database.get_db)):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized", headers={"WWW-Authenticate": "Bearer"})

    auth_token = verify_token(token, cred_exception)

    user = db.query(models.User).filter(
        models.User.id == auth_token.id).first()

    return user
