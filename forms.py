from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ModelWork, PhotographerWork, Photo, Item, Work, StylistWork, User


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ModelWorkForm(forms.ModelForm):
    class Meta:
        model = ModelWork
        exclude = ['owner']


class PhotographerWorkForm(forms.ModelForm):
    class Meta:
        model = PhotographerWork
        exclude = ['owner']


class StylistWorkForm(forms.ModelForm):
    class Meta:
        model = StylistWork
        exclude = ['owner']


class MakeUpWorkForm(forms.ModelForm):
    class Meta:
        model = ModelWork
        exclude = ['owner']
