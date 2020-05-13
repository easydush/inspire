from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.http import response
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.template import context
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404, GenericAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from inspire import settings
from main.forms import CreativeUserForm, CreativeUserChangeForm, PasswordResetForm, PasswordResetRequestForm
from main.models import Company, User
from main.serializers import CompanySerializer
from main.models import UserToken

from main.tasks import send_email_task


def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


def logout_view(request):
    logout(request)
    return redirect('main:index')


def error_500(request):
    return render(request, '500.html', {})


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


# class CompanyView(ListCreateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


# def customhandler404(request, exception, template_name='404.html'):
#     response = render(request, template_name)
#     response.status_code = 404
#     return response
#
#
# def customhandler500(request, template_name='500.html'):
#     response = render(request, template_name)
#     response.status_code = 500
#     return response

class ResetPasswordRequestView(FormView):
    template_name = 'main/reset.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('main:reset_redirect_message')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            user = User.objects.get(email=data)
            token_raw = default_token_generator.make_token(user)
            UserToken.objects.create(user=user, token=token_raw)
            reset_password_link = str('http://localhost:8000') + reverse('main:reset',
                                                                         kwargs={
                                                                             'username': user.username,
                                                                             'token': token_raw
                                                                         }
                                                                         )

            send_email_task.delay(
                subject='Reset password',
                to_email=user.email,
                from_email=settings.EMAIL_HOST_USER,
                template='main/reset_message.html',
                args={'url': reset_password_link}
            )
        return self.form_valid(form)


class UserResetPasswordAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        user = User.objects.get(username=username)
        token = kwargs['token']
        try:
            UserToken.objects.get(user=user, token=token)
        except UserToken.DoesNotExist:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class ResetPasswordView(UserResetPasswordAccessMixin, FormView):
    form_class = PasswordResetForm
    template_name = 'main/reset_conf.html'
    success_url = reverse_lazy('main:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["password"]
            username = kwargs['username']
            token = kwargs['token']
            user_token = UserToken.objects.get(user__username=username, token=token)

            user = user_token.user
            user.set_password(data)
            user.save()

            user_token.delete()

        return self.form_valid(form)


class MessageSentView(TemplateView):
    template_name = 'main/message_sent.html'
