from django.db import models
from django.contrib.auth.models import User


class Breeder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    fluffiness = models.BooleanField(default=False)
    breeder = models.ForeignKey(Breeder, on_delete=models.CASCADE, related_name='cats')

    def __str__(self):
        return self.name
