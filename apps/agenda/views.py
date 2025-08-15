from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Agendamento, Medico
from .forms import AgendarConsultaForm, AgendarExameForm
from django.urls import reverse

@login_required
def agendar_consulta(request):
    if request.method == "POST":
        form = AgendarConsultaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.tipo = Agendamento.TIPO_CONSULTA
            obj.save()
            messages.success(request, "Consulta agendada com sucesso!")
            return redirect(reverse("usuarios:painel_usuario") + "?tab=agendamentos")
    else:
        form = AgendarConsultaForm()
    return render(request, "agenda/agendar_consulta.html", {"form": form})

@login_required
def agendar_exame(request):
    if request.method == "POST":
        form = AgendarExameForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.tipo = Agendamento.TIPO_EXAME
            obj.save()
            messages.success(request, "Exame agendado com sucesso!")
            return redirect(reverse("usuarios:painel_usuario") + "?tab=agendamentos")
    else:
        form = AgendarExameForm()
    return render(request, "agenda/agendar_exame.html", {"form": form})


@login_required
def listar_agendamentos(request):
    itens = (Agendamento.objects
             .select_related("especialidade", "medico", "exame_tipo")
             .filter(usuario=request.user)
             .order_by("data_hora"))
    return render(request, "agenda/listar_agendamentos.html", {"itens": itens})

@login_required
def editar_agendamento(request, pk):
    obj = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
    if obj.tipo == Agendamento.TIPO_CONSULTA:
        FormClass = AgendarConsultaForm
        template = "agenda/agendar_consulta.html"
    elif obj.tipo == Agendamento.TIPO_EXAME:
        FormClass = AgendarExameForm
        template = "agenda/agendar_exame.html"
    else:
        raise Http404

    if request.method == "POST":
        form = FormClass(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Agendamento atualizado.")
            return redirect(reverse("usuarios:painel_usuario") + "?tab=agendamentos")
    else:
        form = FormClass(instance=obj)
    return render(request, template, {"form": form, "edicao": True})

@login_required
@require_POST
def excluir_agendamento(request, pk):
    obj = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
    obj.delete()
    messages.info(request, "Agendamento excluído.")
    return redirect(reverse("usuarios:painel_usuario") + "?tab=agendamentos")

@login_required
def medicos_por_especialidade(request, especialidade_id):
    qs = Medico.objects.filter(ativo=True, especialidade_id=especialidade_id).order_by("nome")
    data = [{"id": m.id, "nome": m.nome} for m in qs]
    return JsonResponse({"medicos": data})
