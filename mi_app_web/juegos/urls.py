from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('menu/', views.menu_principal, name='menu'),
    path('logout/', views.logout_view, name='logout'),
    path('nivel/', views.jugar_nivel, name='jugar_nivel'),
    path('mochila/', views.mochila, name='mochila'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('nivel/<int:id_nivel>/jugar/', views.jugar_nivel, name='jugar_nivel'),
]
