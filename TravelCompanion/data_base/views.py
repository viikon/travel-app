from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data_base.crud import create_comment, read_comment, read_all_comments
from data_base.config import db_helper
from data_base.schemas import Table, CreateTable
from fastapi import Body
from typing import Optional

def get_db():
    db = db_helper.session()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/", response_model=Table)
def add_comment(comment: CreateTable, db: Annotated[Session, Depends(get_db)]):
    new_comment = create_comment(db, comment)
    return new_comment

@router.get("/all_comments/", response_model=list[Table])
def get_all_comments(
    db: Session = Depends(get_db),
    limit: int = 10
):
    comments = read_all_comments(db, limit=limit)
    return comments

@router.get("/{place_id}/", response_model=list[Table])
def get_comment_by_place(place_id: str, db: Session = Depends(get_db)):
    comments = read_comment(db, place_id)
    if not comments:
        raise HTTPException(status_code=404, detail="Отзывы не найдены")
    return comments
