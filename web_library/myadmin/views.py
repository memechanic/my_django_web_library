from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from books.models import Book, Genre, AddBookForm, AddGenreForm
from logger.models import Log
from logger.decorators import action_logger


@action_logger()
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Неверное имя пользователя")
            return render(request, "myadmin/login.html")

        if admin.check_password(password):
            request.session["admin_id"] = admin.id
            request.session["admin_name"] = admin.username
            return redirect("dashboard")
        else:
            messages.error(request, "Неверный пароль")

    return render(request, "myadmin/login.html")

@action_logger()
def logout(request):
    request.session.flush()
    return redirect('home')

@action_logger()
def dashboard(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    form = AddBookForm()

    admin_name = request.session.get("admin_name")
    context = {
        "admin_name": admin_name,
        "books": books,
        "genres": genres,
        "addBookForm": form,
    }
    return render(request, "myadmin/dashboard.html", context)


@action_logger()
def add_book(request):
    admin_name = request.session.get("admin_name")

    if request.method == "POST":
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Книга успешно добавлена")
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, "Проверьте правильность введенных данных")
            context = {
                "admin_name": admin_name,
                "bookForm": form
            }

    else:
        context = {
            "admin_name": admin_name,
            "bookForm": AddBookForm(),
        }
    
    return render(request, 'myadmin/add_book.html', context)


@action_logger()
def add_genre(request):
    admin_name = request.session.get("admin_name")
    genres = Genre.objects.all()
    context = {
        "admin_name": admin_name,
        "genres": genres,
    }

    if request.method == "POST":
        form = AddGenreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Жанр успешно добавлен!")
            return redirect('add-genre')
        else:
            messages.add_message(request, messages.ERROR, "Проверьте правильность введенных данных")
            context = {
                "admin_name": admin_name,
                "bookForm": form
            }
    else:
        form = AddGenreForm()
        context = {
            "admin_name": admin_name,
            "genreForm": form,
            "genres": genres,
        }
    
    return render(request, 'myadmin/add_genre.html', context)


@action_logger()
def delete_genre(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    try:
        genre.delete()
    except Exception as err:
        messages.add_message(request, messages.SUCCESS, f"Ошибка удаления жанра: {err}")
    finally:
        return redirect("add-genre")
    
@action_logger()
def book_detail(request, book_id):
    admin_name = request.session.get("admin_name")
    
    book = Book.objects.get(pk=book_id)

    if request.method == "POST":
        form = AddBookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Книга успешно изменена")
            else:
                messages.add_message(request, messages.ERROR, "Книга не была изменена")
            return redirect("dashboard")
        else:
            messages.add_message(request, messages.ERROR, "Ошибка изменения, проверьте правильность введенных данных")
            context = {
                "admin_name": admin_name,
                "book": book,
                "bookForm": form
            }
            print(form.errors)
    else:
        form = AddBookForm(instance=book)
        context = {
            "admin_name": admin_name,
            "book": book,
            "bookForm": form
        }
    
    return render(request, 'myadmin/book_detail.html', context)


@action_logger()
def delete_book(request, book_id):
    admin_name = request.session.get("admin_name")
    
    book = Book.objects.get(pk=book_id)
    try:
        book.delete()
    except Exception as err:
        messages.add_message(request, messages.ERROR, f"Возникла ошибка при удалении: {err}")
        form = AddBookForm(instance=book)
        context = {
            "admin_name": admin_name,
            "book": book,
            "bookForm": form
        }
        return render(request, 'myadmin/book_detail.html', context)
    else:
        messages.add_message(request, messages.SUCCESS, f"Книга успешно удалена (id: {book_id})")
        return redirect('dashboard')
    

@action_logger()
def logs(request):
    admin_name = request.session.get("admin_name")
    
    logs = Log.objects.all().order_by("-created_at")

    context = {
        "admin_name": admin_name,
        "logs": logs,
    }
    return render(request, "myadmin/logs.html", context)

@action_logger()
def download_logs(request):
    data = list(Log.objects.values())

    response = JsonResponse(data, safe=False)
    response['Content-Disposition'] = 'attachment; filename="logs.json"'
    return response