from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import oauth2
from .. import models, schemas, utils
from ..database import  get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model= List[schemas.PostResponse])
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # to make changes visible in PGadmin
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model= schemas.PostResponse)
def get_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post {id} is not found ")
    return  post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,  detail = f"Post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int ,update_post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,  detail = f"Post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")
    
    post_query.update(update_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return  post_query.first()