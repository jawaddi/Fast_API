from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,Field
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

# create the database if ie doesn't exist
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    # id: int
    title: str 
    author: str 
    description: str
    rating: int 

BOOKS = []
#   {
#     "id": 1,
#     "title": "To Kill a Mockingbird",
#     "author": "Harper Lee",
#     "description": "To Kill a Mockingbird is a novel by Harper Lee published in 1960. It was immediately successful, winning the Pulitzer Prize, and has become a classic of modern American literature.",
#     "rating": 4.5
#   },
#   {
#     "id": 2,
#     "title": "1984",
#     "author": "George Orwell",
#     "description": "1984 is a dystopian novel by George Orwell published in 1949. It is set in a totalitarian regime and explores themes of government surveillance, control, and manipulation of truth.",
#     "rating": 4.4
#   },
#   {
#     "id": 3,
#     "title": "The Great Gatsby",
#     "author": "F. Scott Fitzgerald",
#     "description": "The Great Gatsby is a novel by F. Scott Fitzgerald published in 1925. It is set in the fictional town of West Egg on Long Island and follows the lives of wealthy individuals during the Jazz Age.",
#     "rating": 4.3
#   },
#   {
#     "id": 4,
#     "title": "Pride and Prejudice",
#     "author": "Jane Austen",
#     "description": "Pride and Prejudice is a romantic novel by Jane Austen published in 1813. It follows the story of Elizabeth Bennet and her relationship with the proud Mr. Darcy.",
#     "rating": 4.6
#   },
#   {
#     "id": 5,
#     "title": "Harry Potter and the Sorcerer's Stone",
#     "author": "J.K. Rowling",
#     "description": "Harry Potter and the Sorcerer's Stone is the first novel in the Harry Potter series by J.K. Rowling. It follows the story of a young wizard, Harry Potter, and his adventures at Hogwarts School of Witchcraft and Wizardry.",
#     "rating": 4.8
#   },
#     {
#   "id": 12345,
#   "title": "To Kill a Mockingbird",
#   "author": "Harper Lee",
#   "description": "To Kill a Mockingbird is a novel by Harper Lee published in 1960. It was immediately successful, winning the Pulitzer Prize, and has become a classic of modern American literature.",
#   "rating": 4.5
# }]



# read books
@app.get("/")

async def get_book(db: Session=Depends(get_db)):
    return db.query(models.Books).all()

# create a book
@app.post("/")
async def create_book(book:Book,db: Session=Depends(get_db)):
    # BOOKS.append(book)
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()
    return book


# Update a book
@app.put("/{id}")
async def update_book(book_id: int, book: Book,db: Session=Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id==book_id).first()

    if book_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"The book with id {book_id} was not found"
            )
    
    # book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()

# Delete the book
@app.delete("/{id}")
async def delete_book(book_id: int,db: Session=Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id==book_id).first()


    if book_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"The book with id {book_id} was not found"
            )

    book_model = db.query(models.Books).filter(models.Books.id==book_id).delete()
    db.commit()
