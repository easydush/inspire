from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import main
from . import views
from .views import CompanyViewSet, ResetPasswordView, ResetPasswordRequestView, MessageSentView

app_name = 'main'

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileChangeView.as_view(), name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('api/', include(router.urls)),
    path('reset/', ResetPasswordRequestView.as_view(), name='reset_request'),
    path('reset-password/<username>/<token>', ResetPasswordView.as_view(), name='reset'),
    path('reset-message/', MessageSentView.as_view(), name='reset_redirect_message'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler500 = 'main.views.error_500'
