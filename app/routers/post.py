from .. import models, schemas,oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional
from .. import oauth2
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostVote])
def get_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, 
    skip: int = 0, 
    search: Optional[str] = ""):

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
        .filter(models.Post.title.contains(search)) \
        .group_by(models.Post.id) \
        .limit(limit) \
        .offset(skip) \
        .all()
    
    # Create the response in the required format
    response = [
        {
            "post": {
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "id": post.id,
                "created_at": post.created_at,
                "owner_id": post.owner_id,
                "owner": {
                    "id": post.owner.id,
                    "email": post.owner.email,
                    "created_at": post.owner.created_at
                }
            },
            "votes": votes
        }
        for post, votes in results
    ]

    return response

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)
                 , current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO public."Post" ("Title", "Content", "Published") VALUES (%s, %s, %s) RETURNING *""", 
    #               (post.title, post.content,post.published))
    #new_post = cursor.fetchall()
    #conn.commit()
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#%s prevents sequel injection attacks!!

#careful with structure with data sensitive types like int
@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM public."Post" WHERE "id" = %s """, (str(id),)) #the , is fixing something
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post_data = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
        .filter(models.Post.id == id) \
        .group_by(models.Post.id, models.Post.title, models.Post.content, models.Post.published, models.Post.created_at, models.Post.owner_id) \
        .first()
    
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail =f"Post with id {id} was not found!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"Message": f"Post with id {id} was not found!"}
    post, votes = post_data
    return schemas.PostVote(post=post, votes=votes)


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM public."Post" WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist!")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE public."Post" SET "Title" = %s, "Content" =%s, "Published" =%s WHERE "id" =%s RETURNING *""",
    #                (post.title, post.content,post.published,id))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist!")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()