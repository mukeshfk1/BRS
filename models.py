from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped , mapped_column, DeclarativeBase
from typing import List

class Base(DeclarativeBase):
    pass

#creating a books class for mapping book table
class Books(Base):
    __tablename__ = "books"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    author : Mapped[str] = mapped_column(String)
    title : Mapped[str] = mapped_column(String)
    publication_year : Mapped[int] = mapped_column(Integer)

    book_review : Mapped[List["Review"]] = relationship(back_populates= "review_book")


#creating a review class for mapping review table
class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True)
    book_id : Mapped[int] = mapped_column(ForeignKey("books.id"))
    reviews : Mapped[str] = mapped_column(String)  
    rating : Mapped[int] = mapped_column(Integer)
    email:Mapped[str]  = mapped_column(String)
    review_book : Mapped["Books"] = relationship(back_populates= "book_review")

