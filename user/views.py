from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.shortcuts import render

from django.shortcuts import render, redirect, reverse
from django.template import context

from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View, generic

# Create your views here.
from user.forms import PhotoForm


class AddPhotoView(LoginRequiredMixin, generic.FormView):
    form_class = PhotoForm
    template_name = 'user/forms.html'
    success_url = reverse_lazy('user:forms')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return super(AddPhotoView, self).form_valid(form)
    # def get(self, request):
    #    return render(request, 'user/forms.html', {'form': PhotoForm(), 'form_name': 'Add new photo'})

    # def post(self, request):
    #    form = PhotoForm(request.POST)
    #    if form.is_valid():
    #        photo = form.save()
    #        return redirect(reverse('photo_new'))
    #    return render(request, 'user/forms.html', {'form': form, 'form_name': 'Add new photo'})


class AddPhotographerWorkView(LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    def test_func(self):
        return 'Photographer' in self.request.user.role.title


class AddModelWorkView(LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    def test_func(self):
        return 'Model' in self.request.user.role.title


class AddStylistWorkView(LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    def test_func(self):
        return 'Stylist' in self.request.user.role.title


class AddVisagistWorkView(LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    def test_func(self):
        return 'Visagist' in self.request.user.role.title
