from django.db import models

# Create your models here.


class User(models.Model):
    code = models.CharField(max_length=8, default="", unique=True)
    name = models.CharField(max_length=20, default="", unique=False)
