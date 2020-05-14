from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'works'
urlpatterns = [
    path('photo/', views.PhotoListView.as_view(), name='photo-list'),
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(), name='photo-detail'),
    path('photo/create/', views.PhotoCreateView.as_view(), name='photo-create'),
    path('photo/<int:pk>/update/', views.PhotoUpdateView.as_view(), name='photo-update'),
    path('photo/<int:pk>/delete/', views.PhotoDelete.as_view(), name='photo-delete'),
    path('work/stylist', views.StylistWorksView.as_view(), name='stylistwork-list'),
    path('work/visagist', views.MakeUpWorksView.as_view(), name='makeupwork-list'),
    path('work/photographer', views.PhotographerWorksView.as_view(), name='photographerwork-list'),
    path('work/model', views.ModelWorksView.as_view(), name='modelwork-list'),
    path('work/stylist/create', views.AddStylistWorkView.as_view(), name='stylistwork-add'),
    path('work/visagist/create', views.AddVisagistWorkView.as_view(), name='makeupwork-add'),
    path('work/photographer/create', views.AddPhotographerWorkView.as_view(), name='photographerwork-add'),
    path('work/model/create', views.AddModelWorkView.as_view(), name='modelwork-add'),
]
# for items
urlpatterns += [
    path('item/', views.ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/create/', views.ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item-delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
