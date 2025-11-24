from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, auto_created=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password: str):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password: str):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.username