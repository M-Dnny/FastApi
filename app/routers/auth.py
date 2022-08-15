from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from ..import database, schema, models, utils, oauth


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schema.Token)
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                            "message": "Invalid Credentials"}, )

    # Create token

    access_token = oauth.create_access_token(data={"user_id": user.id})

    return {"token": access_token, "token_type": "Bearer"}
