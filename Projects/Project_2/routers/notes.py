from fastapi import APIRouter, status, HTTPException, Depends, Response
from ..database import get_db
from .. import schemas
from sqlalchemy.orm import Session
from .. import models, aouth2
from typing import List, Optional

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NotesSchema, db: Session = Depends(get_db), current_user: int = Depends(aouth2.get_current_user)):
    new_note = models.Notes(owner_id = current_user.id, **note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {"message": "New note was created sucessfully."}

@router.get("/", response_model = List[schemas.Notes_Response_Schema])
def get_notes(db: Session = Depends(get_db), current_user: int = Depends(aouth2.get_current_user)):
    notes = db.query(models.Notes).all()

    return notes

@router.put("/{id}")
def update_note(id: int, updated_note: schemas.NotesSchema, db: Session = Depends(get_db), current_user: int = Depends(aouth2.get_current_user)):
    note_toBeUpdate = db.query(models.Notes).filter(models.Notes.id == id)
    note = note_toBeUpdate.first()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id: {id} is not found.")
    
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot able change to other user's notes.")

    note_toBeUpdate.update(updated_note.dict(), synchronize_session=False)
    db.commit()

    return {'data': note_toBeUpdate.first()}

@router.get("/{id}")
def get_each_note(id: int, db: Session = Depends(get_db), current_user: int = Depends(aouth2.get_current_user)):
    note = db.query(models.Notes).filter(models.Notes.id == id).first()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id: {id} is not found")
    
    return note

@router.delete("/{id}")
def delete_note(id: int, db: Session = Depends(get_db), current_user: int = Depends(aouth2.get_current_user)):
    note = db.query(models.Notes).filter(models.Notes.id == id)

    
    if note.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id: {id} is not found")

    if note.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Cannot able to delete other user's notes.")

    note.delete(synchronize_session=False)
    db.commit()

    return {"message": f"Note with id: {id} has been deleted sucessfully."}
