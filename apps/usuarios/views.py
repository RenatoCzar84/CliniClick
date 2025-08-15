from django.contrib import messages
from datetime import date
from django.utils import timezone
from apps.agenda.models import Agendamento
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
    idade = _idade(getattr(request.user, "data_nascimento", None))
    agora = timezone.now()

    qs = (Agendamento.objects
          .select_related("especialidade", "medico", "exame_tipo")
          .filter(usuario=request.user))

    proximos = qs.filter(data_hora__gte=agora).order_by("data_hora")[:10]
    anteriores = qs.filter(data_hora__lt=agora).order_by("-data_hora")[:10]

    return render(request, "usuarios/painel.html", {
        "idade": idade,
        "prox_agendamentos": proximos,
        "ant_agendamentos": anteriores,
        "tab": request.GET.get("tab") or "",
    })

def sair_usuario(request):
    logout(request)  # invalida a sessão no backend
    messages.info(request, "Você saiu da sua conta.")
    next_url = request.GET.get("next")
    return redirect(next_url or "index")

@csrf_exempt
def keepalive(request):
    # Aceita POST/GET sem CSRF; só renova se estiver autenticado
    if request.user.is_authenticated:
        request.session.modified = True
    return JsonResponse({"ok": True})

@csrf_exempt
def logout_beacon(request):
    # Opcional: se você ainda usa o beacon em algum lugar
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({"ok": True})

def _idade(dn):
    if not dn:
        return None
    hoje = date.today()
    return hoje.year - dn.year - ((hoje.month, hoje.day) < (dn.month, dn.day))
