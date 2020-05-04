from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Company(models.Model):
    """ This is an user's unnecessary field.
     May be used for company's ambassadors, for example, Max Factor's artist
    """
    title = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)


class User(AbstractUser):
    """ Extension of AbstractUser for adding new fields such as:
    full name, biography, location (country. city) and date of birth
    """
    full_name = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)


class Photographer(User):
    """ This is an extension for extended User """

    def __str__(self):
        return 'Photographer'


class MakeUpArtist(User):
    """ This is an extension for extended User """

    def __str__(self):
        return 'Make up artist'


class Stylist(User):
    """ This is an extension for extended User """

    def __str__(self):
        return 'Stylist'


class SuperModel(User):
    """ This is an extension for extended User """

    def __str__(self):
        return 'Model'


class Photo(models.Model):
    """ This is the one of the main models that will be shown in main app.
     It has model, photographer, make up artist and stylist like a real-world work
      on Instagram or other beauty blogs """
    photo = models.ImageField(upload_to='inspire/photos', blank=True, default='')
    super_models = models.ManyToManyField(SuperModel)
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    make_up_artist = models.ForeignKey(MakeUpArtist, on_delete=models.CASCADE)
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)


class Item(models.Model):
    """ Attribute for someone's work"""
    brand = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Camera(Item):
    """ Additional attribute for Photographer """
    article = models.CharField(max_length=20, blank=True)


class BeautyTip(Item):
    """ Additional attribute for Make Up Artist """
    colour = models.CharField(max_length=20, blank=True)


class Cloth(Item):
    """ Additional attribute for Stylist. That means clothes. """
    colour = models.CharField(max_length=20, blank=True)
    article = models.CharField(max_length=20, blank=True)
    """ Enumeration for item's field season """
    SUMMER = 'summer'
    WINTER = 'winter'
    SPRING = 'spring'
    FALL = 'fall'
    UNIVERSAL = 'any season'
    SEASON_CHOICES = [
        (SUMMER, 'summer'),
        (WINTER, 'winter'),
        (FALL, 'fall'),
        (SPRING, 'spring'),
        (UNIVERSAL, 'any season'),
    ]
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        default=UNIVERSAL,
    )


class Work(models.Model):
    """ This is an album of photos for users' portfolios
    Should be extended for each model to add specific details."""
    title = models.CharField(max_length=15, blank=True)
    photos = models.ManyToManyField(Photo)

    def __str__(self):
        return self.title


class PhotographerWork(Work):
    """ This is an extension of work for Photographer.
    It may be important to select a camera.
    """
    owner = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)


class StylistWork(Work):
    """ This is an extension of work for Stylist."""
    owner = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    style = models.CharField(max_length=15, blank=True)
    items = models.ManyToManyField(Item)


class MakeUpWork(Work):
    """ This is an extension of work for Make Up artist."""
    owner = models.ForeignKey(MakeUpArtist, on_delete=models.CASCADE)
    beauty_tips = models.ManyToManyField(BeautyTip)


class ModelWork(Work):
    """ This is an extension of work for Model."""
    owner = models.ForeignKey(SuperModel, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)


class Portfolio(models.Model):
    """ This is a collection of user's works, something like posts in blog,
     they may be used as a content for profile posts in future"""
    works = models.ManyToManyField(Work)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.owner.username}\'s Portfolio'
