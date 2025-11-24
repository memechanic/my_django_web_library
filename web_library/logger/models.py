from django.db import models

class Log(models.Model):
    METHODS = {
        "P": "POST",
        "G": "GET",
    }
    username = models.CharField(verbose_name="Имя пользователя", max_length=50, null=False)
    status = models.PositiveSmallIntegerField(verbose_name="Статус")
    action = models.CharField(verbose_name="Действие", max_length=300)
    method = models.CharField(verbose_name="Метод", max_length=1, choices=METHODS) # type: ignore
    path = models.CharField(verbose_name="Путь", max_length=300)
    created_at = models.DateTimeField(verbose_name="Дата и время", auto_now_add=True)