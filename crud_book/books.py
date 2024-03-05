from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field

app = FastAPI()
class Book(BaseModel):
    id: int
    title: str = Field(min_length=1)
    author: str = Field(min_length=5,max_length=10)
    description: str = Field(min_length=1,max_length=100)
    rating: int =Field(gt=-1,lt=101)

BOOKS = [
  {
    "id": 1,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "description": "To Kill a Mockingbird is a novel by Harper Lee published in 1960. It was immediately successful, winning the Pulitzer Prize, and has become a classic of modern American literature.",
    "rating": 4.5
  },
  {
    "id": 2,
    "title": "1984",
    "author": "George Orwell",
    "description": "1984 is a dystopian novel by George Orwell published in 1949. It is set in a totalitarian regime and explores themes of government surveillance, control, and manipulation of truth.",
    "rating": 4.4
  },
  {
    "id": 3,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "description": "The Great Gatsby is a novel by F. Scott Fitzgerald published in 1925. It is set in the fictional town of West Egg on Long Island and follows the lives of wealthy individuals during the Jazz Age.",
    "rating": 4.3
  },
  {
    "id": 4,
    "title": "Pride and Prejudice",
    "author": "Jane Austen",
    "description": "Pride and Prejudice is a romantic novel by Jane Austen published in 1813. It follows the story of Elizabeth Bennet and her relationship with the proud Mr. Darcy.",
    "rating": 4.6
  },
  {
    "id": 5,
    "title": "Harry Potter and the Sorcerer's Stone",
    "author": "J.K. Rowling",
    "description": "Harry Potter and the Sorcerer's Stone is the first novel in the Harry Potter series by J.K. Rowling. It follows the story of a young wizard, Harry Potter, and his adventures at Hogwarts School of Witchcraft and Wizardry.",
    "rating": 4.8
  },
    {
  "id": 12345,
  "title": "To Kill a Mockingbird",
  "author": "Harper Lee",
  "description": "To Kill a Mockingbird is a novel by Harper Lee published in 1960. It was immediately successful, winning the Pulitzer Prize, and has become a classic of modern American literature.",
  "rating": 4.5
}]



# read books
@app.get("/")

async def get_book():
    return BOOKS

# create a book
@app.post("/")
async def create_book(book:Book):
    BOOKS.append(book)
    return book


# Update a book
@app.put("/{id}")
async def update_book(id: int, book: Book):
    for index, item_book in enumerate(BOOKS):
        if int(item_book['id']) == id:
            BOOKS[index] = book  # Update the book in the list
            return book
    raise HTTPException(
        status_code=404,
        detail=f"The book with id {id} was not found"
    )

# Delete the book
@app.delete("/{id}")
async def delete_book(id: int):
    for index, item_book in enumerate(BOOKS):
        if int(item_book['id']) == id:
            del BOOKS[index]  # Remove the book at the current index
            return f"The book with id {id} has been deleted!"

    raise HTTPException(
        status_code=404,
        detail=f"The book with id {id} was not found"
    )