from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(payload.password)
    payload.password = hashed_password

    user = models.User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"users id {id} was not found")
    return user
