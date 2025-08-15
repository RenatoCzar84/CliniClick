from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("login/", views.login_usuario, name="login_usuario"),
    path("logout/", views.sair_usuario, name="sair_usuario"),
    path("painel/", views.painel_usuario, name="painel_usuario"),
    path("cadastro/", views.cadastro_usuario, name="cadastro"),
    path("keepalive/", views.keepalive, name="keepalive"),
    path("logout-beacon/", views.logout_beacon, name="logout_beacon"),
]
