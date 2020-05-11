from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class Company(models.Model):
    """ This is an works's unnecessary field.
     May be used for company's ambassadors, for example, Max Factor's artist
    """
    title = models.CharField(max_length=30, blank=True, unique=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'company'
        ordering = ['title']


class Role(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    title = models.SlugField()

    def __str__(self):
        return f'{self.title}'


class User(AbstractUser):
    """ Extension of AbstractUser for adding new fields such as:
    full name, biography, location (country, city) and date of birth
    """
    profile_photo = models.ImageField(upload_to='userprofiles/avatars', blank=True,
                                      default='media/userprofiles/photos/cat.jpg', null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    blog_url = models.URLField(verbose_name="blog url", blank=True, null=True)

    role = models.ManyToManyField(Role)

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    """ This a post that contains and presents works's work"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.title
