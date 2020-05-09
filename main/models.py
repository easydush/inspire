from django.db import models

# Create your models here.
from django.utils import timezone

from user.models import User


class Post(models.Model):
    """ This a post that contains and presents user's work"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.title
