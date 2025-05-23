from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
     prefix="/users",
     tags=["Users"]
)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
     user = db.query(models.User).filter(models.User.id == id).first()
     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
     return user



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
     # Hash the password - user.password
     # hased_password = pwd_context.hash(user.password)
     # user.password = hased_password
     user.password = utils.hash(user.password)
     new_user = models.User(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user) # RETURNING *
     return new_user