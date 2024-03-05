from pydantic import BaseModel, conint

from typing import Optional


class Book(BaseModel):
    title: str
    author:str
    publication_year: int

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author:Optional[str] = None
    publication_year: Optional[int] = None

class Review(BaseModel):
    book_id:int
    reviews:str
    email:str
    rating: conint(ge=0, le=5)

class UpdateReview(BaseModel):
    reviews:Optional[str] = None
    email:Optional[str] = None
    rating: Optional[conint(ge=0, le=5)] = None