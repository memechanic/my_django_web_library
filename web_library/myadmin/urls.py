from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("book-detail/<int:book_id>", views.book_detail, name="book-detail"),
    path("add-book", views.add_book, name="add-book"),
    path("delete-book/<int:book_id>", views.delete_book, name="delete-book"),
    path("logs/", views.logs, name="logs"),
    path("download-logs/", views.download_logs, name="download-logs"),
    path("add-genre", views.add_genre, name="add-genre"),
    path("delete-genre/<int:genre_id>", views.delete_genre, name="delete-genre"),
]
