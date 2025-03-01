from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
     prefix="/posts",
     tags=["Posts"]
) # Replace @app with @router


# @router.get("/", response_model= List[schemas.Post]) # List to avoid potential type errors
@router.get("/", response_model= List[schemas.PostOut])
# def get_posts():
     # posts = cursor.execute("""SELECT * FROM posts""")
     # posts = cursor.fetchall()
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):
     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(
     #      models.Post.title.contains(search)).limit(limit).offset(skip).all()
     # posts = db.query(models.Post).all()

     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
          models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
          models.Post.title.contains(search)).limit(limit).offset(skip).all()
     # print(results)

     return posts



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
     # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # Add the comma at the end to avoid Internal Server Error
     # post = cursor.fetchone()

     # post = db.query(models.Post).filter(models.Post.id == id).first()

     post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
          models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()


     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id: {id} was not found")
     
     # if post.owner_id != current_user.id:
     #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
     #                          detail=f"Not authorized to perform requested action")
     return post




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
     # (post.title, post.content, post.published)) # Avoids SQL injects, order matters like in SQL
     # new_post = cursor.fetchone()
     # conn.commit()
     # new_post = models.Post(title=post.title, content=post.content, published=post.published)

     new_post = models.Post(owner_id=current_user.id,**post.dict()) # Unpack = equivalent of the line above
     db.add(new_post)
     db.commit()
     db.refresh(new_post) # RETURNING *
     return new_post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
     # deleted_post = cursor.fetchone()
     # conn.commit()

     post_query = db.query(models.Post).filter(models.Post.id == id)

     post = post_query.first()

     if post is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"the post with id: {id} was not found")
     
     if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail=f"Not authorized to perform requested action")

     post_query.delete(synchronize_session=False)
     db.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
     # (post.title, post.content, post.published, id),)
     # updated_post = cursor.fetchone()
     # conn.commit()

     post_query = db.query(models.Post).filter(models.Post.id == id)

     post  = post_query.first()

     if post is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id: {id} does not exist")
     
     if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail=f"Not authorized to perform requested action")

     post_query.update(updated_post.dict(), synchronize_session=False)

     db.commit()

     return post_query.first()