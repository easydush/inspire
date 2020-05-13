from django.conf import settings
from django.db.models import F
from django.db import models
from django.urls import reverse

from main.models import User, Company


class Photo(models.Model):
    """ This is the one of the main models that will be shown in main app.
     It has model, photographer, make up artist and stylist like a real-world work
      on Instagram or other beauty blogs """
    title = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to='userprofiles/photos', blank=True, default='media/userprofiles/photos/cat.jpg')
    super_models = models.ManyToManyField(User)
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photographer')
    make_up_artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='makeupartist')
    stylist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stylist')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by',
                                   null=True)

    def get_absolute_url(self):
        return reverse('works:photo-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + ' ' + self.created_by.username

    class Meta:
        db_table = 'photo'


class Item(models.Model):
    """ Attribute for someone's work"""
    brand = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='added_by',
                                 null=True)
    colour = models.CharField(max_length=20, blank=True, null=True)
    article = models.CharField(max_length=20, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'brand']


class Work(models.Model):
    """ This is an album of photos for users' portfolios
    Should be extended for each model to add specific details."""
    title = models.CharField(max_length=15, blank=True)
    photos = models.ManyToManyField(Photo)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class PhotographerWork(Work):
    """ This is an extension of work for Photographer.
    It may be important to select a camera.
    """
    phowner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_by')

    class Meta:
        db_table = 'photographer_work'


class StylistWork(Work):
    """ This is an extension of work for Stylist."""
    stowner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='styled_by')
    style = models.CharField(max_length=15, blank=True)

    class Meta:
        db_table = 'stylist_work'


class MakeUpWork(Work):
    """ This is an extension of work for Make Up artist."""
    mkowner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='made_by')

    class Meta:
        db_table = 'makeup'


class ModelWork(Work):
    """ This is an extension of work for Model."""
    mdowner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='model_by')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = 'model_work'

# class Portfolio(models.Model):
#     """ This is a collection of works's works, something like posts in blog,
#      they may be used as a content for profile posts in future"""
#     works = models.ManyToManyField(Work)
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.owner.username}\'s Portfolio'
#
#     class Meta:
#         db_table = 'portfolio'
