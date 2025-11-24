from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from .models import Book, Genre
from logger.decorators import action_logger

@action_logger()
def index(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    context = {
        "books": books, 
        "genres": genres
    }
    return render(request,"books/index.html", context)

@action_logger()
def books_by_theme(request, genre_id):
    books = Book.objects.filter(genre=genre_id)
    genres = Genre.objects.all()
    
    context = {
        "books": books, 
        "genres": genres
    }
    return render(request,"books/index.html", context)

@action_logger()
def download_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return FileResponse(book.file_url.open("rb"), as_attachment=True)