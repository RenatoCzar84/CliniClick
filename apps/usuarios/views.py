from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .forms import UsuarioForm


def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Usuário criado com sucesso! Faça login abaixo.')
                # redireciona para a Home (onde está o form de login no header)
                return redirect('index')
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Verifique CPF/usuário/email já existentes.")
        # se inválido ou deu IntegrityError, re-renderiza com erros (sem limpar)
        return render(request, 'usuarios/cadastro.html', {'form': form, 'limpar': False})
    else:
        # GET: renderiza com campos limpos (para burlar autocomplete)
        form = UsuarioForm()
        return render(request, 'usuarios/cadastro.html', {'form': form, 'limpar': True})


def login_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('username', '').strip()
        senha = request.POST.get('password', '')
        proximo = request.POST.get('next') or request.GET.get('next')

        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')

            # Se veio ?next=/algum/caminho, usa esse caminho; senão, painel do usuário
            destino = proximo if proximo else reverse('usuarios:painel_usuario')
            return redirect(destino)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

@login_required
def sair_usuario(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    # pode mandar pra home ou para a rota de login do namespace
    return redirect('usuarios:login')


@login_required
def painel_usuario(request):
    """Página interna do usuário após login."""
    return render(request, 'usuarios/painel.html', {'usuario': request.user})


@login_required
def sair_usuario(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('index')  # ou 'login_usuario' se preferir voltar ao form de login


# ===== Apoio à expiração de sessão (popup/JS) =====

@csrf_exempt
def logout_beacon(request):
    # navigator.sendBeacon faz POST simples sem CSRF; por isso csrf_exempt
    if request.method == 'POST':
        logout(request)
        return HttpResponse('ok')
    return HttpResponse(status=405)


@login_required
def keepalive(request):
    # renova a sessão
    request.session.modified = True
    return HttpResponse(status=204)

