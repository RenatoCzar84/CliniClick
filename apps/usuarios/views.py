from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UsuarioForm
from django.views.decorators.csrf import csrf_exempt

def cadastro_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login para acessar seu painel.")
            return redirect("index")  # sua home no apps.base
    else:
        form = UsuarioForm()
    return render(request, "usuarios/cadastro.html", {"form": form})

def login_usuario(request):
    next_url = request.GET.get("next") or request.POST.get("next")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Bem-vindo(a) de volta!")
            return redirect(next_url or "usuarios:painel_usuario")
        messages.error(request, "Credenciais inválidas.")
    return redirect("index")  # login está no navbar da base

@login_required
def painel_usuario(request):
    return render(request, "usuarios/painel.html")

def sair_usuario(request):
    logout(request)  # invalida a sessão no backend
    messages.info(request, "Você saiu da sua conta.")
    next_url = request.GET.get("next")
    return redirect(next_url or "index")

def keepalive(request):
    # só tocar a sessão
    request.session.modified = True
    return JsonResponse({"ok": True})

def logout_beacon(request):
    # usado pelo sendBeacon ao expirar
    logout(request)
    return HttpResponse(status=204)
