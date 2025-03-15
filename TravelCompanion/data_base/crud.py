from sqlalchemy.orm import Session
from sqlalchemy import select
from api.places_app.config import LIMIT
from data_base.models import UserComment
from data_base.schemas import Table, CreateTable


def create_comment(db: Session, table: CreateTable):
    comment_table = UserComment(
        place_id=table.place_id,
        user_name=table.user_name,
        comment=table.comment,
        rating=table.rating
    )

    db.add(comment_table)
    db.commit()
    db.refresh(comment_table)
    
    return comment_table


def read_comment(db: Session, place_id: str, skip: int = 0, limit: int = LIMIT):
    query = select(UserComment).where(UserComment.place_id == place_id).offset(skip).limit(limit)
    result = db.execute(query)
    
    return result.scalars().all()


def read_all_comments(db: Session, limit: int = 10):
    query = select(UserComment).limit(limit)
    result = db.execute(query)

    return result.scalars().all()
