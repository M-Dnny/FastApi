from typing import List, Optional
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import session
from sqlalchemy import func


from ..import models, schema, oauth
from ..database import get_db

routers = APIRouter(
    prefix="/post",
    tags={"Posts"}
)

# Get Posts


@routers.get("/get", response_model=List[schema.PostOut])
async def get_post(db: session = Depends(get_db), current_user: int = Depends(oauth.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):

    my_post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(
        skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    print("RESULTS: ", results)
    return results

# My Post


@routers.get("/mypost", response_model=List[schema.PostOut])
async def get_post(db: session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # my_post = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()

    my_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id).all()

    return my_post

#  Create Post


@routers.post("/createpost", status_code=status.HTTP_201_CREATED, response_model_include=schema.Post)
async def create_post(post: schema.CreatePost, db: session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    insert_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(insert_post)
    db.commit()
    db.refresh(insert_post)
    return {"data": insert_post}

# Get by ID


@routers.get("/getinfo/{id}", response_model=schema.PostOut)
async def getInfo(id: int,  db: session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    # post = findPost(id)

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found!")
    return post


# Delete post

@routers.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def post_delete(id: int, db: session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    # index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorize to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {"data": 'deleted'}

# Update post


@routers.put("/update/{id}", response_model=schema.Post)
async def update_post(id: int, post_update: schema.UpdatePost, db: session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorize to perform this action")

    post_query.update(post_update.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
