from django.shortcuts import render

from django.shortcuts import render, redirect, reverse
from django.template import context

from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from django.views import View, generic

# Create your views here.
from user.forms import PhotoForm
from user.models import Role


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


class ModelAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        role = Role.objects.get(title='Model')
        if not request.user.is_authenticated and role not in request.user.role:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class VisagistAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        role = Role.objects.get(title='Visagist')
        if not request.user.is_authenticated and role not in request.user.role:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StylistAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        role = Role.objects.get(title='Stylist')
        if not request.user.is_authenticated and role not in request.user.role:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PhotographAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        role = Role.objects.get(title='Photograph')
        if not request.user.is_authenticated and role not in request.user.role:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
