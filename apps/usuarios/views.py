from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Usuário criado com sucesso! Faça login abaixo.')
                # ajuste o nome da rota da sua home se for diferente de 'index'
                return redirect('index')
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Verifique CPF/usuário/email já existentes.")
        # se inválido, cai para o render abaixo com os erros
        return render(request, 'usuarios/cadastro.html', {'form': form, 'limpar': False})
    else:
        form = UsuarioForm()
        return render(request, 'usuarios/cadastro.html', {'form': form, 'limpar': True})


def cadastro_sucesso(request):
    return render(request, 'usuarios/cadastro_sucesso.html')


def login_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('username', '').strip()
        senha = request.POST.get('password', '')
        proximo = request.POST.get('next') or request.GET.get('next')

        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
            return redirect(proximo or 'painel_usuario')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            # volta para a página de origem (ou home) para reexibir o form do header
            return redirect(request.META.get('HTTP_REFERER', '/'))

    # GET: não temos página de login dedicada; manda para a home
    return redirect('/')    


# === PÁGINA PROTEGIDA DO USUÁRIO ===
@login_required
def painel_usuario(request):
    """
    Página interna do usuário após login.
    Crie o template 'usuarios/painel.html' herdando de base/base.html.
    """
    return render(request, 'usuarios/painel.html', {'usuario': request.user})


# === LOGOUT ===
@login_required
def sair_usuario(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('login_usuario')  # ou: return redirect('cadastro_usuario') / home
