from django.conf import settings
from django.db.models import F
from django.db import models

from main.models import User, Company


class Photo(models.Model):
    """ This is the one of the main models that will be shown in main app.
     It has model, photographer, make up artist and stylist like a real-world work
      on Instagram or other beauty blogs """
    photo = models.ImageField(upload_to='media/userprofiles/photos', blank=True, default='')
    super_models = models.ManyToManyField(User)
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photographer')
    make_up_artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='makeupartist')
    stylist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stylist')

    class Meta:
        db_table = 'photo'


class Item(models.Model):
    """ Attribute for someone's work"""
    brand = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'brand']


class Camera(Item):
    """ Additional attribute for Photographer """
    article = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'camera'


class BeautyTip(Item):
    """ Additional attribute for Make Up Artist """
    colour = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'beautytip'


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

    class Meta:
        db_table = 'cloth'


class Work(models.Model):
    """ This is an album of photos for users' portfolios
    Should be extended for each model to add specific details."""
    title = models.CharField(max_length=15, blank=True)
    photos = models.ManyToManyField(Photo)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class PhotographerWork(Work):
    """ This is an extension of work for Photographer.
    It may be important to select a camera.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)

    class Meta:
        db_table = 'photographer_work'


class StylistWork(Work):
    """ This is an extension of work for Stylist."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    style = models.CharField(max_length=15, blank=True)
    items = models.ManyToManyField(Item)

    class Meta:
        db_table = 'stylist_work'


class MakeUpWork(Work):
    """ This is an extension of work for Make Up artist."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    beauty_tips = models.ManyToManyField(BeautyTip)

    class Meta:
        db_table = 'makeup'


class ModelWork(Work):
    """ This is an extension of work for Model."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = 'model_work'


class Portfolio(models.Model):
    """ This is a collection of user's works, something like posts in blog,
     they may be used as a content for profile posts in future"""
    works = models.ManyToManyField(Work)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.owner.username}\'s Portfolio'

    class Meta:
        db_table = 'portfolio'
