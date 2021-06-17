from django.db import models
from datetime import datetime


# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    birth_date = models.DateTimeField()
    email = models.EmailField()
    cellphone_number = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='mulima_app/static/mulima_app/avatar', blank=True)
    friends = models.ManyToManyField('self')

    def __str__(self):
        return self.first_name


class Message(models.Model):
    author = models.ForeignKey('Person', on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=datetime.now())

    def __str__(self):
        return "write by: " + self.author.username


class Post(models.Model):
    author = models.ForeignKey('Person', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='mulima_app/static/mulima_app/images', blank=True)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=datetime.now())

    def __str__(self):
        return "write by: " + self.author.username
