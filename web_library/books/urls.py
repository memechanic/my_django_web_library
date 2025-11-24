from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("books_by_theme/<int:genre_id>", views.books_by_theme, name="books_by_theme"),
    path("download-book/<int:book_id>/", views.download_book, name="download-book"),
]
