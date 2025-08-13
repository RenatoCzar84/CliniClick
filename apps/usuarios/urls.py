from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'usuarios'

urlpatterns = [
    # Cadastro
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),

    # Login / Logout
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='base/index.html',   # <— usa a Home ao renderizar
            authentication_form=LoginForm
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Recuperação de senha (deixamos pronto)
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='usuarios/password_reset_form.html',
            email_template_name='usuarios/password_reset_email.txt',
            subject_template_name='usuarios/password_reset_subject.txt',
            success_url=reverse_lazy('usuarios:password_reset_done'),
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='usuarios/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='usuarios/password_reset_confirm.html',
            success_url=reverse_lazy('usuarios:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='usuarios/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]




