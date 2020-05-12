from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from . import views
from .views import CompanyView, SingleCompanyView

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileChangeView.as_view(), name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('companies/', CompanyView.as_view()),
    path('companies/<int:pk>', SingleCompanyView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# router = DefaultRouter()
# router.register('companies', CompanyView, basename='user')
# urlpatterns += [
#     path('api/', include((router.urls, 'main'))),
#     path('api-token-refresh', refresh_jwt_token),
#     path('api-token-auth', obtain_jwt_token),
# ]
