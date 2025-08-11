from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Cadastro
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),

    # Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # Login/Logout (LoginView usa template usuarios/login.html que criaremos)
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Recuperação de senha (templates customizados que vamos criar)
    path('senha/reset/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset.html',
        email_template_name='usuarios/password_reset_email.html',
        subject_template_name='usuarios/password_reset_subject.txt',
        success_url='/usuarios/senha/reset/enviado/'
    ), name='password_reset'),

    path('senha/reset/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html'
    ), name='password_reset_done'),

    path('senha/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuarios/password_reset_confirm.html',
        success_url='/usuarios/senha/reset/feito/'
    ), name='password_reset_confirm'),

    path('senha/reset/feito/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuarios/password_reset_complete.html'
    ), name='password_reset_complete'),
]
