from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.views import View

from main.forms import CreativeUserForm


def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


class RegisterView(View):
    def get(self, request):
        return render(request, 'main/registration.html', {'form': CreativeUserForm()})

    def post(self, request):
        form = CreativeUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'main/registration.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'main/login.html', {'form': AuthenticationForm})

    # really low level
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

            return redirect(reverse('profile'))


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # surveys = Survey.objects.filter(created_by=request.user).all()
        # assigned_surveys = SurveyAssignment.objects.filter(assigned_to=request.user).all()

        #
        return render(request, 'user/profile.html', context)
