from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.template import context
from django.views import View

from main.forms import CreativeUserForm, CreativeUserChangeForm


def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


def popular(request):
    return render(request, 'popular.html', {})


def logout_view(request):
    logout(request)
    return redirect('main:index')


class RegisterView(View):
    def get(self, request):
        return render(request, 'main/registration.html', {'form': CreativeUserForm()})

    def post(self, request):
        form = CreativeUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(True)
            form.save_m2m()
            return redirect(reverse('login'))

        return render(request, 'main/registration.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'main/login.html', {'form': AuthenticationForm})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'main/login.html',
                    {'form': form, 'invalid_creds': True}
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'main/login.html',
                    {'form': form, 'invalid_creds': True}
                )
            login(request, user)

            return redirect(reverse('main:profile'))


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'main/profile.html', {})


class ProfileChangeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'main/profile_edit.html', {'form': CreativeUserChangeForm(instance=request.user)})

    def post(self, request):
        form = CreativeUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('main:profile'))

        return render(request, 'main/profile_edit.html', {'form': form})
