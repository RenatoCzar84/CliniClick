from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Cadastro
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('cadastro/sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),

    # Login/Logout
    path('login/', views.UsuarioLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # Recuperação de senha (templates customizados)
    path('senha/reset/', PasswordResetView.as_view(
        template_name='usuarios/password_reset.html'
    ), name='password_reset'),
    path('senha/reset/enviado/', PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html'
    ), name='password_reset_done'),
    path('senha/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='usuarios/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('senha/reset/completa/', PasswordResetCompleteView.as_view(
        template_name='usuarios/password_reset_complete.html'
    ), name='password_reset_complete'),
]

