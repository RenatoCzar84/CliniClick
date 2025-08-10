from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.urls import reverse

from django.contrib.auth.views import LoginView

from .forms import UsuarioSignupForm, UsuarioProfileForm


def cadastro_usuario(request):
    """Cadastro com validação de CPF único e senha com hash (UserCreationForm)."""
    if request.method == 'POST':
        form = UsuarioSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # UserCreationForm cuida do hash
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            # redireciona para nossa rota de login tradicional
            return redirect('usuarios:login')
        else:
            messages.error(request, 'Revise os campos destacados.')
    else:
        form = UsuarioSignupForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})


class UsuarioLoginView(LoginView):
    """Login tradicional (usuário/e-mail + senha). Template nosso, e botão Google via allauth."""
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True


def cadastro_sucesso(request):
    return render(request, 'usuarios/cadastro_sucesso.html')


@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
        else:
            messages.error(request, 'Corrija os campos indicados.')
    else:
        form = UsuarioProfileForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

