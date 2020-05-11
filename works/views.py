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
from works.forms import PhotoForm
from works.models import Photo


class PhotoCreateView(LoginRequiredMixin, generic.FormView):
    form_class = PhotoForm
    template_name = 'works/photo_add.html'
    success_url = reverse_lazy('works:photo-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        form.save_m2m()
        return super(PhotoCreateView, self).form_valid(form)


class PhotoListView(generic.ListView):
    model = Photo
    context_object_name = 'photos'


class PhotoDetailView(generic.DetailView):
    model = Photo


class PhotoUpdateView(generic.UpdateView):
    model = Photo
    fields = ['title', 'photo' ,'super_models', 'photographer', 'stylist', 'make_up_artist']
    template_name = 'works/photo_update.html'


class PhotoDelete(generic.DeleteView):
    model = Photo
    success_url = reverse_lazy('works:photo-list')
    template_name = 'works/photo_delete.html'


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
