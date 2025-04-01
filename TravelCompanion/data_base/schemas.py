from pydantic import BaseModel, validator

class CreateTable(BaseModel):
    place_id: str
    user_name: str
    comment: str
    rating: int


    @validator('rating')
    def validate_rating(cls, value):
        if not (0 <= value <= 5):
            raise ValueError('Rating must be between 0 and 5')
        return value

class Table(CreateTable):
    id: int  
