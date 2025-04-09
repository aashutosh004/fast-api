from fastapi import FastAPI
from pydantic import BaseModel ## for defining the guidelines for structre/syntax of requests
from typing import List


app = FastAPI()

class Book(BaseModel):
    id: int
    name: str
    author: str

books: List[Book] = []

## Fast Api works on Decorators

@app.get("/")
def read_root():
    return {"message": "Welcome Folks!!!"}

@app.get("/books")
def get_books():
    return books

@app.post("/books")
def add_book(book: Book):
    books.append(book)
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            print("Book info updated successfully")
            return updated_book
    
    return {"error": "Book not found"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        deleted_book = books.pop(index)
        print("Book deleted successfully")
        return deleted_book
    
    return {"error": "Book not found"}