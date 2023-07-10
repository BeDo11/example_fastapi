from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResp)
async def create_posts(payload: schemas.PostCreate, db: Session = Depends(get_db), 
                       current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (payload.title, payload.content, payload.published))
    #post = cursor.fetchone()
    #conn.commit()
    post = models.Post(owner_id=current_user.id, **payload.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    #post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if None == post_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResp)
async def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if None == post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"put with id {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized")
   
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()