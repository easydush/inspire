from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ModelWork, PhotographerWork, Photo, BeautyTip, Camera, Item, Cloth, Work, StylistWork, Portfolio, \
    User



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'


class BeautyTipForm(forms.ModelForm):
    class Meta:
        model = BeautyTip
        fields = '__all__'


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'


class ClothForm(forms.ModelForm):
    class Meta:
        model = Cloth
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


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        exclude = ['owner']
