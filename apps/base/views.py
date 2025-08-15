from django.shortcuts import render
from django.utils import timezone
from apps.agenda.models import Especialidade, Medico, ExameTipo, Agendamento

def index(request):
    return render(request, 'base/index.html')

def index(request):
    stats = {
        "especialidades": Especialidade.objects.count(),
        "medicos": Medico.objects.filter(ativo=True).count(),
        "exames": ExameTipo.objects.filter(ativo=True).count(),
        "agendamentos_hoje": Agendamento.objects.filter(
            data_hora__date=timezone.localdate()
        ).count(),
    }
    especialidades = Especialidade.objects.order_by("nome")[:6]
    return render(request, "base/index.html", {"stats": stats, "especialidades": especialidades})

# Create your views here.
