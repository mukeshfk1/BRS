from typing import Union
from starlette .responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import schemas, models, utils, database
from sqlalchemy import select
from sqlalchemy.orm import joinedload


app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(url="/docs/")


@app.get('/books/')
def get_book(
             publication_year: Optional[int]=None,
             author:Optional[str]=None,

              db = Depends(database.get_db)):
    """
    This Endpoint is for fetching books from daatbase with filter on author and publication year
    """
    try:
        db_book = select(models.Books)

        if publication_year:
            db_book = db_book.where(models.Books.publication_year == publication_year)
            
        if author:
            db_book = db_book.where(models.Books.author == author)

        db_book = db.scalars(db_book).all()
       
        if not db_book:
            return JSONResponse(status_code=404, content = { "detail":"no books found"})
        
        return JSONResponse(status_code=200, content = {"data":db_book})

        
    except Exception as err:
        return {"error_detail":str(err)}

@app.post('/books/')
def add_book(payload: schemas.Book, db=Depends(database.get_db)):
    """
     This Endpoint is for adding new book in the database
    """
    try:
        db_book = select(models.Books).where(models.Books.title == payload.title)
        db_book = db.scalars(db_book).all()
        
        if db_book:
            return JSONResponse(status_code=403, content = { "detail":"book already exists"})
        new_book = models.Books()
        new_book.author = payload.author
        new_book.title = payload.title
        new_book.publication_year = payload.publication_year

        db.add(new_book)
        db.commit()
        db.refresh(new_book)
       

        return JSONResponse(status_code=201, content = { "detail":"new book has been added"})

        
    except Exception as err:
        db.rollback()
        return JSONResponse(status_code=400, content = { "detail":str(err)})

@app.put('/books/')
def update_book(book_id:int, 
                payload: schemas.UpdateBook, 
                db=Depends(database.get_db)):
    """
     This Endpoint is for updating existing book in the database
    """
    try:
        
        db_book = db.get(models.Books, book_id)
        
        if not db_book:
            return JSONResponse(status_code=404, content = { "detail":"invalid book_id exists"})
        
        payload = dict(payload)
        for key in payload:
            if payload[key]:
                setattr(db_book, key, payload[key])
        

        
        db.commit()
        db.refresh(db_book)
       

        return JSONResponse(status_code=200, content = { "detail":"book has been updated"})

        
    except Exception as err:
        db.rollback()
        return JSONResponse(status_code=400, content = { "detail":str(err)})

@app.delete('/books/')
def delete_book(book_id:int, 
                db=Depends(database.get_db)):
    """
     This Endpoint is for deleting an existing book in the database
    """
    try:
        
        db_book = db.get(models.Books, book_id)
        
        if not db_book:
            return JSONResponse(status_code=404, content = { "detail":"invalid book_id exists"})
        
        db.delete(db_book)
        db.commit()
       

        return {"detail":"book has been deleted"}

        
    except Exception as err:
        db.rollback()
        return JSONResponse(status_code=400, content = { "detail":str(err)})



@app.get('/reviews/')
def get_reviews(
            book_id: int,
            db = Depends(database.get_db)):
    """
    This Endpoint is for fetching all reviews of a specific book
    """
    try:
        db_book = select(models.Books).where(models.Books.id == book_id).options(joinedload(models.Books.book_review))

        db_book = db.scalars(db_book).unique().all()
       
        if not db_book:
            return JSONResponse(status_code=404, content = { "detail":"no book found"})
        
        return JSONResponse(status_code=200, content = {"data":db_book})

        
    except Exception as err:
        return {"error_detail":str(err)}

@app.post('/reviews/')
def add_review(payload: schemas.Review, db=Depends(database.get_db)):
    """
     This Endpoint is for adding a book review in the database
     rating should be from 0 to 5
    """
    try:
        
        db_book = db.get(models.Books, payload.book_id)

        # to check wheather the book exists or not
        if not db_book:
            return JSONResponse(status_code=400, content = { "detail":"invalid book_id"})
        
        db_review = select(models.Review).where(models.Review.email == payload.email)
        db_review = db.scalars(db_review).all()

        # to prevent the duplicate entry of any reviewer
        if db_review:
            return JSONResponse(status_code=400, content = { "detail":f"review already exixst for {payload.email}"})

        new_review = models.Review()
        new_review.book_id = payload.book_id
        new_review.reviews = payload.reviews
        new_review.rating = payload.rating
        new_review.email = payload.email

        db.add(new_review)
        db.commit()
        db.refresh(new_review)
       

        return JSONResponse(status_code=201, content={"detail":"new review has been added","data":new_review})
        
    except Exception as err:
        db.rollback()
        return JSONResponse(status_code=400, content = { "detail":str(err)})


@app.put('/reviews/')
def update_review(
                    review_id:int, 
                    payload: schemas.UpdateReview, 
                    db=Depends(database.get_db)
                ):
    """
     This Endpoint is for updating a book review in the database
     
    """
    try:
        
        db_review = db.get(models.Review, review_id)
        
        if not db_review:
            return JSONResponse(status_code=400, content = { "detail":"invalid review_id"})
        
        payload = dict(payload)
        for key in payload:
            if payload[key]:
                setattr(db_review, key, payload[key])

        
        db.commit()
        db.refresh(db_review)
       

        return JSONResponse(status_code=200, content={"detail":"review has been updated"})

        
    except Exception as err:
        db.rollback()
        return JSONResponse(status_code=400, content = { "detail":str(err)})


@app.delete('/reviews/')
def delete_review(review_id:int, 
                db=Depends(database.get_db)):
    """
     This Endpoint is for deleting an existing book review in the database
    """
    try:
        
        db_review = db.get(models.Review, review_id)
        
        if not db_review:
            return JSONResponse(status_code=404, content = { "detail":"invalid review_id exists"})
        
        db.delete(db_review)
        db.commit()
       

        return {"detail":"review has been deleted"}

        
    except Exception as err:
        db.rollback()
        return JSONResponse(status_code=400, content = { "detail":str(err)})

