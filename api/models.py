from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    preferences = models.CharField(max_length=255, blank=True)

class WatchedAnime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime_id = models.IntegerField()
    title = models.CharField(max_length=255)
