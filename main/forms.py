from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import User


class CreativeUserForm(UserCreationForm):
    birth_date = forms.DateField(required=False, input_formats=['%Y-%m-%d', '%m/%d/%Y',
                                                                '%m/%d/%y', '%d.%m.%Y'])

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'first_name', 'last_name', 'email',
                  'role', 'birth_date', 'profile_photo', 'bio',
                  'location', 'birth_date', 'company', 'blog_url')


class CreativeUserChange(UserChangeForm):
    class Meta:
        model = User
        fields = ('profile_photo', 'bio', 'location', 'birth_date',
                  'company', 'blog_url')
