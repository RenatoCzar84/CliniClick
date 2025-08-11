from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.db import IntegrityError

from .forms import UsuarioForm, UsuarioProfileForm

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
                return redirect('login')  # usaremos o LoginView do Django/Allauth via template próprio
            except IntegrityError as e:
                form.add_error(None, "Erro ao salvar os dados. Verifique se CPF, e-mail ou username já estão em uso.")
        # se inválido, cai pro render abaixo com erros
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

def cadastro_sucesso(request):
    return render(request, 'usuarios/cadastro_sucesso.html')

@login_required
def perfil(request):
    """Exibe os dados do usuário logado."""
    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user
    })

@login_required
def editar_perfil(request):
    """Edita dados permitidos (não altera e-mail/CPF). Suporta upload de foto."""
    if request.method == 'POST':
        form = UsuarioProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = UsuarioProfileForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def logout_view(request):
    """Logout seguro com mensagem + redirecionamento para home."""
    auth_logout(request)
    messages.info(request, 'Você saiu da sua conta com segurança.')
    return redirect('index')  # rota da home em apps.base (ajuste se o nome for outro)


