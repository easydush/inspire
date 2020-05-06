from django.shortcuts import render

from django.shortcuts import render, redirect, reverse
from django.template import context
from django.views import View

# Create your views here.
from user.forms import PhotoForm


class AddPhotoView(View):
    def get(self, request):
        return render(request, 'user/photo_edit.html', {'form': PhotoForm(), 'form_name': 'Add new photo'})

    def post(self, request):
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.save()
            return redirect(reverse('photo_new'))

        return render(request, 'user/photo_edit.html', {'form': form, 'form_name': 'Add new photo'})
