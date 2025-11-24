from django import forms

from django.db import models
from django.forms import ModelForm

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)

    def __str__(self) -> str:
        return self.name

class AddGenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control col"})
        }

def download_filename(instance, filename):
        new_title = instance.title.lower().replace(' ', '_')
        new_author = instance.author.lower().replace(' ', '_')
        new_filename = f"{new_author}_{new_title}.{str(filename).split('.')[-1]}"
        return f"books/{new_filename}"

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название", unique=True)
    author = models.CharField(max_length=150, verbose_name="Автор")
    description = models.TextField(verbose_name="Описание")
    cover_image = models.ImageField(upload_to="covers/", verbose_name="Обложка")
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name="Жанр",
    )
    rating = models.PositiveSmallIntegerField(default=0, verbose_name="Рейтинг")

    file_url = models.FileField(upload_to=download_filename, verbose_name="Файл книги")
    
    def __str__(self):
        return f"{self.title} — {self.author}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-id"]


class AddBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "genre", "rating", "cover_image", "file_url"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "rating": forms.Select(attrs={"class": "form-select"}, choices=[(r, r) for r in range(6)])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ["genre", "rating"]:
                field.widget.attrs['class'] = "form-control"
            elif name == "genre":
                field.widget.attrs['class'] = "form-select"
