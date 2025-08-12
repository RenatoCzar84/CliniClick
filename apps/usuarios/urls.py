from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'usuarios'

urlpatterns = [
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='usuarios/login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

