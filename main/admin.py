from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from main.forms import CreativeUserForm, CreativeUserChangeForm
from main.models import Company, Role, User, UserToken

admin.site.register(Company)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(UserToken)

class CreativeUserAdmin(UserAdmin):
    add_form = CreativeUserForm
    form = CreativeUserChangeForm
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name', 'bio', 'profile_photo']
