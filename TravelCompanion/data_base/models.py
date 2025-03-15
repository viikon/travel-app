from sqlalchemy import String, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from data_base.config import CreateTableHelper


class UserComment(CreateTableHelper):
    place_id: Mapped[str] = mapped_column(String(30))
    user_name: Mapped[str] = mapped_column(String(30))
    comment: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating_range'),
    )
