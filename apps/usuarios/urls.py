from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_usuario, name='login_usuario'),
    path('sair/', views.sair_usuario, name='sair_usuario'),
    path('painel/', views.painel_usuario, name='painel_usuario'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
]
