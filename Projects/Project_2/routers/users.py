from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, hashing
from ..database import get_db

router = APIRouter(prefix= "/users", tags=["User"])

@router.post("/", response_model=schemas.UserResponseModel)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    user.password = hashing.hash(user.password)

    user_data = models.User(**user.dict())

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return user_data

@router.get("/{id}", response_model=schemas.UserResponseModel)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id of {id} is not found.")
    
    return user
