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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
