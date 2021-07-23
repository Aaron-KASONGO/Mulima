from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date_born = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=datetime.now())

    def __str__(self):
        return "write by: " + self.author.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.FileField(upload_to='files_post', blank=True)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=datetime.now())

    def __str__(self):
        return "write by: " + self.author.username
