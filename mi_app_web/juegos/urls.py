from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('niveles/', views.niveles_view, name='niveles'),
    path('menu/', views.menu_view, name='menu'),
]
