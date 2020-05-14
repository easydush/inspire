from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View, generic

# Create your views here.
from works.forms import PhotoForm, ItemForm, ModelWorkForm, PhotographerWorkForm, StylistWorkForm, MakeUpWorkForm
from works.models import Photo, Item, StylistWork, ModelWork, PhotographerWork, MakeUpWork


class PhotoCreateView(LoginRequiredMixin, generic.FormView):
    form_class = PhotoForm
    template_name = 'works/photo_add.html'
    success_url = reverse_lazy('works:photo-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        user = form.save(commit=False)
        form.save_m2m()

        return super(PhotoCreateView, self).form_valid(form)


class PhotoListView(generic.ListView):
    model = Photo
    context_object_name = 'photos'


class PhotoDetailView(generic.DetailView):
    model = Photo


class PhotoUpdateView(generic.UpdateView):
    model = Photo
    fields = ['title', 'photo', 'super_models', 'photographer', 'stylist', 'make_up_artist']
    template_name = 'works/photo_update.html'


class PhotoDelete(generic.DeleteView):
    model = Photo
    success_url = reverse_lazy('works:photo-list')
    template_name = 'works/photo_delete.html'


class AddPhotographerWorkView(LoginRequiredMixin, generic.FormView):
    form_class = PhotographerWorkForm
    template_name = 'works/work_add.html'
    success_url = reverse_lazy('works:photographerwork-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        form.save_m2m()
        return super(AddPhotographerWorkView, self).form_valid(form)


class AddModelWorkView(LoginRequiredMixin, generic.FormView):
    form_class = ModelWorkForm
    template_name = 'works/work_add.html'
    success_url = reverse_lazy('works:modelwork-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        form.save_m2m()
        return super(AddModelWorkView, self).form_valid(form)


class AddStylistWorkView(LoginRequiredMixin, generic.FormView):
    form_class = StylistWorkForm
    template_name = 'works/work_add.html'
    success_url = reverse_lazy('works:stylistwork-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        form.save_m2m()
        return super(AddStylistWorkView, self).form_valid(form)


class AddVisagistWorkView(LoginRequiredMixin, generic.FormView):
    form_class = MakeUpWorkForm
    template_name = 'works/work_add.html'
    success_url = reverse_lazy('works:makeupwork-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        form.save_m2m()
        return super(AddVisagistWorkView, self).form_valid(form)


class StylistWorksView(LoginRequiredMixin, generic.ListView):
    model = StylistWork
    context_object_name = 'works'


class MakeUpWorksView(LoginRequiredMixin, generic.ListView):
    model = MakeUpWork
    context_object_name = 'works'


class ModelWorksView(LoginRequiredMixin, generic.ListView):
    model = ModelWork
    context_object_name = 'works'


class PhotographerWorksView(LoginRequiredMixin, generic.ListView):
    model = PhotographerWork
    context_object_name = 'works'


class ItemCreateView(LoginRequiredMixin, generic.FormView):
    form_class = ItemForm
    template_name = 'works/item_add.html'
    success_url = reverse_lazy('works:item-list')

    def form_valid(self, form):
        form.save()
        return super(ItemCreateView, self).form_valid(form)


class ItemListView(generic.ListView):
    model = Item
    context_object_name = 'items'


class ItemDetailView(generic.DetailView):
    model = Item


class ItemUpdateView(generic.UpdateView):
    model = Item
    fields = '__all__'
    template_name = 'works/item_update.html'


class ItemDelete(generic.DeleteView):
    model = Item
    success_url = reverse_lazy('works:item-list')
    template_name = 'works/item_delete.html'
