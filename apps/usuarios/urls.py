from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path('sair/', views.sair_usuario, name='logout'),
    path('painel/', views.painel_usuario, name='painel_usuario'),

    # usados pelo popup
    path('logout-beacon/', views.logout_beacon, name='logout_beacon'),
    path('keepalive/', views.keepalive, name='keepalive'),
]
