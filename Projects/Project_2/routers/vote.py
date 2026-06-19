from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, database, models, aouth2

router = APIRouter(
    prefix="/votes",
    tags=['Vote']
)

@router.post("/")
def vote_post(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(aouth2.get_current_user)):
    is_vote_exits = db.query(models.Notes).filter(models.Notes.id == vote.post_id).first()

    if is_vote_exits is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} deos not exits.")
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    # User wants to add Vote:
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}.")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote."}
    
    else: # User want to delete Vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote not found.")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote."}