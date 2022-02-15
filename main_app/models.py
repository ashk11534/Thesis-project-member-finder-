
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    university = models.ForeignKey(University, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(default='avatar.png', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participants')
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    description = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RoomMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class UserMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    body = models.TextField()


